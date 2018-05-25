# -*- coding: utf-8 -*-
import argparse
import gzip
import logging
import lzma
import time
import zlib

import lz4.frame
import msgpack
import simplejson

logger = logging.getLogger(__name__)


class CompressBenchmark(object):

    def __init__(self, data):
        self.data = data

    def lzmaCompress(self, b, level=1):
        return lzma.compress(b, preset=level)

    def gzipCompress(self, b, level=1):
        return gzip.compress(b, compresslevel=level)

    def zlibCompress(self, b, level=1):
        return zlib.compress(b, level)

    def lz4Compress(self, b, level=1):
        return lz4.frame.compress(b, compression_level=level)

    def lzmaDecompress(self, b):
        return lzma.decompress(b)

    def gzipDecompress(self, b):
        return gzip.decompress(b)

    def zlibDecompress(self, b):
        return zlib.decompress(b)

    def lz4Decompress(self, b):
        return lz4.frame.decompress(b)

    def msgpackEncode(self, o):
        return msgpack.packb(o)

    def msgpackDecode(self, b):
        return msgpack.unpackb(b)

    def jsonEncode(self, o):
        return simplejson.dumps(o)

    def jsonDecode(self, b):
        return simplejson.loads(b)

    def benchmark(self, iteration):
        """
        测试
        """
        originLength = len(self.data) / 1024
        logger.info('origin length: {}KiB'.format(originLength))

        _ = self.lzmaCompress(b)
        lzmaLength = len(_) / 1024
        logger.info('lzma length: {}KiB'.format(lzmaLength))

        # lzma compress
        ts = time.time()
        for i in range(iteration):
            self.lzmaCompress(b)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('lzma compress timecost: {}ms'.format(tc))

        # lzma decompress
        ts = time.time()
        for i in range(iteration):
            self.lzmaDecompress(_)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('lzma decompress timecost: {}ms'.format(tc))

        # == gzip ==
        _ = self.gzipCompress(b)
        gzipLength = len(_) / 1024
        logger.info('gzip length: {}KiB'.format(gzipLength))

        # gzip compress
        ts = time.time()
        for i in range(iteration):
            self.gzipCompress(b)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('gzip compress timecost: {}ms'.format(tc))

        # gzip decompress
        ts = time.time()
        for i in range(iteration):
            self.gzipDecompress(_)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('gzip decompress timecost: {}ms'.format(tc))

        # == zlib ==
        _ = self.zlibCompress(b)
        zlibLength = len(_) / 1024
        logger.info('zlib length: {}KiB'.format(zlibLength))

        # zlib compress
        ts = time.time()
        for i in range(iteration):
            self.zlibCompress(b)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('zlib compress timecost: {}ms'.format(tc))

        # zlib decompress
        ts = time.time()
        for i in range(iteration):
            self.zlibDecompress(_)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('zlib decompress timecost: {}ms'.format(tc))

        # == zlib lv2 ===
        _ = self.zlibCompress(b, 2)
        zlibLength = len(_) / 1024
        logger.info('zlib lv2 length: {}KiB'.format(zlibLength))

        # zlib compress
        ts = time.time()
        for i in range(iteration):
            self.zlibCompress(b, 2)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('zlib compress lv2 timecost: {}ms'.format(tc))

        # zlib decompress
        ts = time.time()
        for i in range(iteration):
            self.zlibDecompress(_)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('zlib decompress lv2 timecost: {}ms'.format(tc))

        # == lz4 ==
        _ = self.lz4Compress(b)
        lz4Length = len(_) / 1024
        logger.info('lz4 length: {}KiB'.format(lz4Length))

        # lz4 compress
        ts = time.time()
        for i in range(iteration):
            self.lz4Compress(b)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('lz4 compress timecost: {}ms'.format(tc))

        # lz4 decompress
        ts = time.time()
        for i in range(iteration):
            self.lz4Decompress(_)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('lz4 decompress timecost: {}ms'.format(tc))

        # == simplejson ==
        o = self.jsonDecode(b)
        e = self.jsonEncode(o)
        _ = len(e) / 1024
        logger.info('simplejson length: {}'.format(_))

        ts = time.time()
        for i in range(iteration):
            self.jsonEncode(o)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('simplejson encode timecost: {}ms'.format(tc))

        ts = time.time()
        for i in range(iteration):
            self.jsonDecode(e)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('simplejson decode timecost: {}ms'.format(tc))

        # == msgpack ==
        e = self.msgpackEncode(o)
        _ = len(e) / 1024
        logger.info('msgpack length: {}'.format(_))

        ts = time.time()
        for i in range(iteration):
            self.msgpackEncode(o)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('msgpack encode timecost: {}ms'.format(tc))

        ts = time.time()
        for i in range(iteration):
            self.msgpackDecode(e)
        te = time.time()
        tc = (te - ts) * 1000
        logger.info('msgpack decode timecost: {}ms'.format(tc))


logging.basicConfig(level=logging.INFO)
ap = argparse.ArgumentParser()
ap.add_argument('--data', required=True)
ap.add_argument('--iteration', default=1000, type=int)
options = ap.parse_args()

with open(options.data, 'rb') as f:
    b = f.read()

ben = CompressBenchmark(b)
ben.benchmark(options.iteration)
