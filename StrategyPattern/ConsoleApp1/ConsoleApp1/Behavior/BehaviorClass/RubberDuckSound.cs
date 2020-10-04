using ConsoleApp1.Behavior.Interface;
using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApp1.Behavior.BehaviorClass
{
    class RubberDuckSound : ISound
    {
        public void Sound()
        {
            Console.WriteLine("꽉곽");
        }
    }
}
