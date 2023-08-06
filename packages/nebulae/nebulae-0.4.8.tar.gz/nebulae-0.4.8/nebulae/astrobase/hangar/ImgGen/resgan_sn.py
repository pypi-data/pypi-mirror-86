#!/usr/bin/env python
'''
garage
Created by Seria at 03/01/2019 8:32 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-
from ... import dock
from .architect import SNResG, SNResD, BN


class Discriminator(dock.Craft):
    def __init__(self, in_shape, norm_fn, scope='DSC'):
        super(Discriminator, self).__init__(scope)
        H, W, C = in_shape
        self.backbone = SNResD(in_shape, norm_fn)
        self.cls = dock.SN(dock.Dense(H * W * 4, 1))

    def run(self, x):
        x = self.backbone(x)
        self['out'] = self.cls(x)

        return self['out']



class SNResGAN(dock.Craft):
    def __init__(self, in_shape, latent_dim=128, norm_fn=BN, scope='SNRESGAN'):
        super(SNResGAN, self).__init__(scope)
        self.G = SNResG(in_shape, latent_dim, norm_fn)
        self.D = Discriminator(in_shape, norm_fn)

    def run(self):
        pass