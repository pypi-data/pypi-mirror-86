#!/usr/bin/env python
# coding=utf-8

import sys
import json
import wave
import numpy as np
from scipy.io import wavfile
from matplotlib import pyplot as plt


digits = '123a456b789c*0#d'
frequencies = [
    697, 770, 852, 941,         # rows
    1209, 1336, 1477, 1633      # columns
]


def csum(num):
    retv = 10
    while num:
        retv ^= (num & 0xf) ^ 0xf
        num >>= 4
    return retv & 0xf


def make_code(number):
    return "#%d%s" % (number, digits[csum(number)])


def validate_code(code):
    """
    Verify if a code is valid; return its value if it is, False otherwise.
    """
    if code[0][1] != "#":
        return False
    try:
        value = int("".join(c[1] for c in code[1:-1]))
    except Exception:
        return False
    return digits[csum(value)] == str(code[-1][1]) and value


class Tones:
    def __init__(self, sample_rate=44100, length=.1, silence=0.05):
        self.period = np.pi * 2 / sample_rate
        self.length = int(1. * sample_rate * length)
        self.silence = np.zeros(int(1. * sample_rate * silence))
        self.table = {idx: self._gen_tone(idx) for idx in range(16)}

    def _gen_tone(self, idx):
        row = frequencies[idx / 4]
        column = frequencies[4 + idx % 4]
        return .5 * np.hstack([np.array([
            np.sin(phase * row * self.period) +
            np.sin(phase * column * self.period)
            for phase in range(self.length)
        ]), self.silence])

    def sequence(self, string):
        return np.hstack([self.table[digits.index(sym)] for sym in string])


def write_wav(filename, data, sample_rate=44100):
    out = wave.open(filename, 'w')
    # nchannel, sampwidth, framerate, nframes, comptype, compname
    out.setparams((1, 2, sample_rate, 0, 'NONE', 'not compressed'))
    out.writeframes((data * 32767).astype(np.int16).tostring())
    out.close()


def write_test_pattern(filename="test-pattern.wav", duration=10, srate=44100):
    tones = Tones(srate)
    data = np.zeros(srate * duration)
    for i in range(duration):
        tone_waves = tones.sequence(make_code(i))
        s = i * srate
        e = s + tone_waves.shape[0]
        data[s:e] = tone_waves
    write_wav(filename, data, srate)


if __name__ == '__main__':
    write_test_pattern()
#
# plt.style.use('ggplot')
# plt.figure(figsize=(16, 4))
#
# # TODO: try to separate the signals before processing, we might have
# # a better DTMF
#
#
#
#
# class Goertzel:
#     def __init__(self, sample_rate, freq, idx):
#         self.idx = idx
#         period = freq * 1. / sample_rate
#         self.w_real = 2.0 * np.cos(2.0 * np.pi * period)
#         self.mov_avg = .0
#         self.delta_mov_avg = .0
#         n = .05 * sample_rate / 128
#         self.n1 = (n - 1) / n
#         self.n2 = 1 / n
#
#     def power(self, samples):
#         d1, d2 = 0.0, 0.0
#         for s in samples:
#             y = s + self.w_real * d1 - d2
#             d2, d1 = d1, y
#         retv = d2 ** 2 + d1 ** 2 - self.w_real * d1 * d2
#         mov_avg = self.mov_avg * self.n1 + retv * self.n2
#         self.delta_mov_avg = mov_avg - self.mov_avg
#         self.mov_avg = mov_avg
#         return retv
#
#     def reset(self):
#         self.mov_avg = .0
#         self.delta_mov_avg = .0
#
#     def active(self):
#         return self.delta_mov_avg < 0 and self.mov_avg > 30
#
#
# class Detector:
#
#     def __init__(self, sample_rate, signal=.1, silence=.05):
#         self.sample_rate = sample_rate
#         self.signal_samples = int(sample_rate * signal)
#         self.silence_samples = int(sample_rate * silence)
#         self.max_signal_size = self.signal_samples * 13
#         self.max_signal_size += self.silence_samples * 14
#         self.template = (
#             [0] * self.silence_samples +
#             [1] * self.signal_samples +
#             [0] * self.silence_samples
#         )
#         self.filters = [
#             Goertzel(sample_rate, f, i // 2)
#             for i, f in enumerate(self.frequencies)
#         ]
#         self._frame_start_filters = [self.filters[idx] for idx in 3, 4, 6]
#
#     def reset(self):
#         for f in self.filters:
#             f.reset()
#
#     def find_frame_start(self, samples):
#         for f in self._frame_start_filters:
#             f.power(samples)
#         row = self._frame_start_filters[0].active()
#         cols = [f.active() for f in self._frame_start_filters[1:]]
#         return row and (cols[0] or cols[1])
#
#     def filter_state(self):
#         return [
#             (f.mov_avg, f.delta_mov_avg) for f in self._frame_start_filters
#         ]
#
#     # def extract_digits(self):
#     #     plt.clf()
#     #     start_pos = self.cur_sample - len(self.buffer)
#     #     x_axis = np.arange(start_pos, self.cur_sample)
#     #     plt.plot(x_axis, self.buffer, "#ee6633")
#     #     plt.ylim([-1.5, 1.5])
#     #     s = np.correlate(np.abs(self.buffer), self.template, "valid")
#     #     mx = s.argmax()
#     #     ts = start_pos + mx
#     #     n = int(self.sample_rate * .05)
#     #
#     #     # [0] * mx + self.template
#     #     plt.plot(x_axis[mx:mx + len(self.template)], self.template, "k")
#     #     code = []
#     #     color = "b"
#     #     for i in range(self.tpl_length):
#     #         p = [f.power(self.buffer[mx:mx + n * 2]) for f in self.filters]
#     #         row = np.argmax(p[:4])
#     #         col = np.argmax(p[4:])
#     #         d = self.digits[row * 4 + col]
#     #         if i == self.tpl_length - 1:
#     #             try:
#     #                 d_idx = csum(int("".join(code[1:])))
#     #                 color = "r" if self.digits[d_idx] != d else "#00ff00"
#     #             except ValueError:
#     #                 color = "k"
#     #         plt.annotate(
#     #             d, xy=(start_pos + mx + n * .75, 0),
#     #             fontsize=60, color=color, weight="bold"
#     #         )
#     #         code.append(d)
#     #         mx += n * 3
#     #     # mng = plt.get_current_fig_manager()
#     #     # mng.resize(*mng.window.maxsize())
#     #     plt.savefig(
#     #         ("plots/control-%05s.png" % ("".join(code[1:-1])))
#     #         .replace(" ", "0")
#     #     )
#     #     if self.codes:
#     #         idx = (ts - self.codes[0][0]) // self.sample_rate
#     #         hpos = idx * self.sample_rate + self.codes[0][0]
#     #         plt.vlines([hpos], [-2], [2], "m")
#     #     # plt.show()
#     #     if code[0] == "#" and color == "#00ff00":
#     #         self.codes.append((ts, "".join(code[1:-1])))
#     #     # requires all codes to be recognized successfully
#     #     # clen = len("%d" % len(self.codes))
#     #     # if clen > self.tpl_length - 2:
#     #     #     self.update_template(clen)
#     #
#     #     # requires the recognition of 9, 99, 999, ...
#     #     if all(c == '9' for c in code[1:-1]):
#     #         self.update_template(self.tpl_length - 1)
#     #     with open("control.json", 'w') as out:
#     #         json.dump(self.codes, out)
#     #     print self.codes
#     #     plt.waitforbuttonpress()
#
#     def decode_digit(self, samples):
#         self.reset()
#         p = [f.power(samples) for f in self.filters]
#         row = np.argmax(p[:4])
#         col = np.argmax(p[4:])
#         return self.digits[row * 4 + col], p[row] + p[4 + col]
#
#     def extract_code(self, samples, start, max_length=13):
#         # plt.clf()
#         # plt.plot(samples, "#ee6633")
#         # plt.ylim([-1.5, 1.5])
#         code = []
#         p = 0
#         ref_power = []
#         for i in range(max_length):
#             e = p + len(self.template) + int(self.silence_samples * 1.5)
#             s = self.align_template(samples[p:e]) + p + self.silence_samples
#             p = s + self.signal_samples
#             digit, power = self.decode_digit(samples[s:p])
#             print s, p, digit, power
#             # plt.vlines([s], [-2], [2], "#00ff00")
#             # plt.vlines([p + self.silence_samples / 2], [-2], [2], "#00ffff")
#             # plt.annotate(
#             #     digit, xy=(s + self.silence_samples * .75, 0),
#             #     fontsize=60, color="g", weight="bold"
#             # )
#             p -= self.silence_samples / 2  # give a small compression margin
#             if len(ref_power) < 3:
#                 ref_power.append(power)
#             else:
#                 print power / np.mean(ref_power)
#                 if power / np.mean(ref_power) < .1:
#                     break
#             code.append((float(start + s) / self.sample_rate, digit))
#         value = validate_code(code)
#         if value is False:
#             self.end_sample = start + self.signal_samples * 2
#         else:
#             self.end_sample = p + self.silence_samples + start
#         print value
#         # print "end_sample", self.end_sample
#         # plt.waitforbuttonpress()
#         return value, code
#
#     def align_template(self, samples):
#         # plt.clf()
#         # plt.plot(samples, "#ee6633")
#         s = np.correlate(np.abs(samples), self.template, "valid")
#         retv = s.argmax()
#         # plt.vlines([retv + self.silence_samples], [-2], [2], "#00ff00")
#         # plt.vlines([retv + self.silence_samples + self.signal_samples],
#         #            [-2], [2], "#00ffff")
#         # plt.waitforbuttonpress()
#         return retv
#         # mx = s.argmax()
#         # n = int(self.sample_rate * .05)
#         #
#         # plt.plot([-.1] * mx + self.template, "k")
#         # code = []
#         # color = "b"
#         # for i in range(self.tpl_length):
#         #     p = [f.power(self.buffer[mx:mx + n * 2]) for f in self.filters]
#         #     row = np.argmax(p[:4])
#         #     col = np.argmax(p[4:])
#         #     d = self.digits[row * 4 + col]
#         #     if i == self.tpl_length - 1:
#         #         try:
#         #             d_idx = csum(int("".join(code[1:])))
#         #             color = "r" if self.digits[d_idx] != d else "#00ff00"
#         #         except ValueError:
#         #             color = "k"
#         #     plt.annotate(
#         #         d, xy=(start_pos + mx + n * .75, 0),
#         #         fontsize=60, color=color, weight="bold"
#         #     )
#         #     code.append(d)
#         #     mx += n * 3
#         # mng = plt.get_current_fig_manager()
#         # mng.resize(*mng.window.maxsize())
#         # plt.waitforbuttonpress()
#         # plt.savefig(
#         #     ("plots/control-%05s.png" % ("".join(code[1:-1])))
#         #     .replace(" ", "0")
#         # )
#
#
# # ats = AudibleTimestampScanner("session=2/wifi-android.wav", [[0, 10000000]])
# # sample_rate, data = wavfile.read("session=2/control.wav")
# # sample_rate, data = wavfile.read("session=2/wifi-android.wav")
#
# # dataset = "control"
# # dataset = "wifi-android"
# # dataset = "mobile-android"
# dataset = "mobile-iphone"
#
# sample_rate, data = wavfile.read("session=2/%s.wav" % dataset)
# dtmf = DTMFDetector(sample_rate)
#
# # data = data[48000 * 84:, 0].astype(float)
# data = data[:, 0].astype(float)
# data /= np.abs(data).max()
#
# win_len = 128
# win = np.hamming(win_len)
#
# scan_range = data.shape[0] // win_len * 2
# idx = 0
#
# codes = []
#
# while idx < scan_range:
#     # find frame start
#     dtmf.reset()
#     while idx < scan_range:
#         print idx, "\r",
#         sys.stdout.flush()
#         s = idx * win_len / 2
#         if s + win_len > len(data):
#             idx = scan_range
#             break
#         samples = data[s:s + win_len]  # * win
#         if dtmf.find_frame_start(samples):
#             break
#         idx += 1
#     if idx == scan_range:
#         break
#     print
#     s = max(s - int(dtmf.silence_samples * 2.5), 0)
#     e = s + dtmf.max_signal_size
#     value, code = dtmf.extract_code(data[s:e], s)
#     if value:
#         codes.append((value, code))
#     print value, code
#     # # -=-=-=-=-=-=-=-
#     # plt.clf()
#     # plt.plot(data[s:e], "#ee6633")
#     # plt.ylim([-1.5, 1.5])
#     # for d in code:
#     #     plt.vlines([d[0] - s], [-2], [2], "#00ff00")
#     #     plt.vlines([d[0] - s + dtmf.signal_samples], [-2], [2], "#00ffff")
#     #     plt.annotate(
#     #         d[1], xy=(d[0] - s + dtmf.silence_samples * .75, 0),
#     #         fontsize=60, color="r" if value is False else "g", weight="bold"
#     #     )
#     # plt.waitforbuttonpress()
#     idx = int(dtmf.end_sample / win_len * 2)
#
#
# with open("session=2/%s.json" % dataset, 'w') as out:
#     json.dump(codes, out)
