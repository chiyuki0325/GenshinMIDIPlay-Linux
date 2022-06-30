#!/usr/bin/python
import asyncio, sys, subprocess
from asyncio.subprocess import PIPE
from asyncio import create_subprocess_exec

if(len(sys.argv)==4):
    exec('from '+sys.argv[2].replace('.py','')+' import keymap')
    synthdriver=sys.argv[3]
elif(len(sys.argv)==3):
    exec('from '+sys.argv[2].replace('.py','')+' import keymap')
    synthdriver='pulseaudio'
elif(len(sys.argv)==2):
    if(sys.argv[1]=='-h' or sys.argv[1]=='--help'):
        print("原神 Linux 风物之诗琴 / 镜花之琴自动演奏脚本")
        print("By YidaozhanYa")
        print("")
        print("参数一：MIDI 文件名")
        print("参数二：键盘映射表文件名")
        print("参数三（可选）：FluidSynth 合成器驱动（alsa/pulseaudio）")
        print("")
        print("需要系统中装有 FluidSynth")
        exit()
    else:
        print("参数错误！")
        exit()
else:
    print("参数错误！")
    exit()

async def _read_stream(stream,):
    while True:
        line = await stream.readline()
        if line:
            if line[0:17]==b'event_post_noteon':
                note=int(line[18:-1].decode("UTF8").split(' ')[1])
                subprocess.Popen(['xdotool','key',keymap[note]])
        else:
            break

async def run(command):
    process = await create_subprocess_exec(*command, stdout=PIPE, stderr=PIPE)
    print("正在自动演奏 ...")
    await asyncio.wait([asyncio.create_task(_read_stream(process.stdout))])
    process.wait()


async def main():
    await run(['stdbuf','-oL','fluidsynth','-a'+synthdriver,sys.argv[1],'-d'])


if __name__ == "__main__":
    asyncio.run(main())
