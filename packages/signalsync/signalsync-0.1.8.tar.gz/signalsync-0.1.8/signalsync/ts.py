# coding=utf-8

"""
Timestamp Set data model
"""

import os
import re
import cv2
import json
import numpy as np
from collections import namedtuple

timestamp_re = re.compile(
    r"(?P<time>\d+(?:\.\d+)?)"          # 1234 | 1234.56
    r"#(?P<csum>\w+)"                   # #3f
    r"(?:&(?P<last>\d+\.\d+))?"         # &16.7
    r"(?:\s+(?P<paylod>.*))?$"          # ' asdasd'
)


Range = namedtuple("Range", "start end t0 period")
Frame = namedtuple("Frame", "time idx last payload")


class TimestampSet:
    def __init__(self):
        self.ranges = []  # the last range is the whole video
        self.frames = []

    def detect_ranges(self, max_frame_gap=500):
        if not self.frames:
            return
        last = start = self.frames[0].idx
        for f in self.frames[1:]:
            if f.idx - last > max_frame_gap:
                self.ranges.append(Range(start, last, 0, 0))
                start = f.idx
            last = f.idx
        if last != start:
            self.ranges.append(Range(start, last, 0, 0))

    def add_full_range(self):
        self.ranges.append(Range(0, -1, 0, 0))

    def reconstruct(self):
        import numpy as np
        for i, r in enumerate(self.ranges):
            if r.start == 0 and r.end == -1:
                frames = self.frames
            else:
                frames = [f for f in self.frames if r.start <= f.idx <= r.end]
            indices = [float(f.idx) for f in frames]
            b = [float(f.time) for f in frames]
            A = np.vstack([indices, np.ones_like(indices)])
            period, t0 = np.linalg.lstsq(A.T, b)[0]
            self.ranges[i] = r._replace(t0=t0, period=period)

    def dump(self):
        return dict(version=1, frames=self.frames, ranges=self.ranges)

    def load(self, dct):
        if dct.get("version") != 1:
            raise ValueError("unsupported version")
        self.ranges = [Range(*r) for r in dct.get("ranges")]
        self.frames = [Frame(*f) for f in dct.get("frames")]

    @staticmethod
    def from_file(path):
        ts = TimestampSet()
        ts.load(json.load(open(path)))
        return ts

    def dump_markers(self, relative=False):
        r = 0 if not relative else self.t0
        return "\n".join("%d,%.3f" % (f.idx, f.time - r) for f in self.frames)


class Video:
    def __init__(self, path):
        print(path)
        metapath = os.path.splitext(path)[0] + ".meta.json"
        self.meta = TimestampSet.from_file(metapath)
        self.t0 = self.meta.ranges[-1].t0
        self.source = cv2.VideoCapture(path)
        w = self.source.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        h = self.source.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        self.aspect = w / h

    def fps(self):
        return self.source.get(cv2.cv.CV_CAP_PROP_FPS)

    def duration(self):
        return self.source.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT) / self.fps()

    def get_frame(self, time):
        time -= self.meta.ranges[-1].t0
        if time < 0:
            return None
        self.source.set(cv2.cv.CV_CAP_PROP_POS_MSEC, time * 1000)
        ok, frame = self.source.read()
        # if ok:
        #     ret, corners = cv2.findChessboardCorners(
        #         cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (7, 5), None
        #     )
        #     print(ret)
        #     if ret:
        #         cv2.drawChessboardCorners(frame, (7, 5), corners, ret)
        return frame  # if ok else None


class VideoSet:
    def __init__(self, folder_path, width=640):
        self.videos = [
            Video(os.path.join(folder_path, fname))
            for fname in os.listdir(folder_path)
            if fname.lower().endswith((".mp4", "webm"))
        ]
        if not self.videos:
            return
        width = int(width / len(self.videos))
        height = int(width / self.videos[0].aspect)
        self.shape = (width, height)

    def start(self, m=min):
        return m(v.t0 for v in self.videos)

    def end(self, m=max):
        return m(v.t0 + v.duration() for v in self.videos)

    def fps(self):
        return max(v.fps() for v in self.videos)

    def get_frame(self, time):
        frames = []
        for v in self.videos:
            frame = v.get_frame(time)
            if frame is None:
                frame = np.zeros(self.shape[::-1] + (3, ), dtype=np.uint8)
            else:
                frame = cv2.resize(frame, self.shape)
            frames.append(frame)
        return cv2.hconcat(frames)

    def convert(self, path, start_m=min, end_m=max):
        t0 = self.start(start_m)
        fno = 0
        fps = self.fps()
        end = self.end(end_m)
        total_frames = (end - t0) * fps
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        w, h = self.shape
        w *= len(self.videos)
        writer = cv2.VideoWriter(path, fourcc, fps, (w, h), True)
        while fno < total_frames:
            if fno % (fps * 300) == 0:
                print("%d / %d" % (fno, total_frames))
            f = self.get_frame(fno / fps + t0)
            writer.write(f)
            fno += 1
            cv2.imshow("all", f)
            if cv2.waitKey(1) & 0xff == 27:
                break
        writer.release()


def convert_old():
    ts = TimestampSet()
    folder = "/media/data/scidata/project=dttp/unit=001/"
    fnames = (
        "2018-03-14 10:39:17 374XDPHH.ts.json",
        "2018-03-14 10:36:16 366YBPHH.ts.json"
    )
    for fname in fnames:
        dct = json.load(open(os.path.join(folder, fname)))
        dct["version"] = 1
        dct["ranges"] = []
        dct["frames"] = [
            f if len(f) == 4 else f + [""]
            for f in dct["detected_frames"]
        ]
        ts.load(dct)
        ts.detect_ranges()
        ts.ranges.pop()
        # ts.add_full_range()
        ts.reconstruct()
        dct = ts.dump()
        dct["note"] = "only first range considered"
        with open(os.path.join(folder, fname[:-7] + "meta.json"), 'w') as out:
            json.dump(dct, out, indent=2)


if __name__ == '__main__':
    vs = VideoSet("/media/data/scidata/project=dttp/unit=001/", 640)
    vs.convert("/media/data/scidata/project=dttp/unit=001/overview.mkv")
    # t0 = t = vs.start() + 150
    # fno = 0
    # fps = vs.fps()
    # print(fps)
    # end = vs.end()
    # while t < end:
    #     f = vs.get_frame(t)
    #     cv2.imshow("all", f)
    #     fno += 50
    #     t = fno / fps + t0
    #     print(t)
    #     if cv2.waitKey(0) & 0xff == 27:
    #         break
