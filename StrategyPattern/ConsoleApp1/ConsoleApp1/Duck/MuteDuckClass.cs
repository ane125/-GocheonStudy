using ConsoleApp1.Behavior.Interface;
using ConsoleApp1.Duck.Base;
using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApp1.Duck
{
    class MuteDuckClass : SuperDuck
    {
        public MuteDuckClass(IDisplay display, ISound sound)
        {
            this.dispay = display;
            this.sound = sound;
        }
    }
}
