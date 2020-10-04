using ConsoleApp1.Behavior.Interface;
using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApp1.Duck.Base
{
    class SuperDuck
    {
        protected IDisplay dispay;
        protected ISound sound;

        public void Display()
        {
            dispay.Display();
        }

        public void Sound()
        {
            sound.Sound();
        }
    }
}
