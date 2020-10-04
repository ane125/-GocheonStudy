using ConsoleApp1.Behavior.Interface;
using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApp1.Behavior.BehaviorClass
{
    class MuteDuckSound : ISound
    {
        public void Sound()
        {
            Console.WriteLine("시발");
        }
    }
}
