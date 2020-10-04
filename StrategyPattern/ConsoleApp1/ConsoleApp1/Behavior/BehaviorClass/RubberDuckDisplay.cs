using ConsoleApp1.Behavior.Interface;
using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApp1.Behavior.BehaviorClass
{
    class RubberDuckDisplay : IDisplay
    {
  
            public void Display()
            {
                Console.WriteLine("나는 고무 오리");
            }
    }
}
