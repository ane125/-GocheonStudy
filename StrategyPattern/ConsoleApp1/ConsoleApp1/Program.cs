using ConsoleApp1.Behavior.BehaviorClass;
using ConsoleApp1.Behavior.Interface;
using ConsoleApp1.Duck;
using ConsoleApp1.Duck.Base;
using System;

namespace ConsoleApp1
{
    class Program
    {
        static void Main(string[] args)
        {
            SuperDuck[] arryDuck = new SuperDuck[5];

            arryDuck[0] = new RubberDuckClass(new RubberDuckDisplay(),new RubberDuckSound());
            arryDuck[1] = new RubberDuckClass(new RubberDuckDisplay(), new RubberDuckSound());
            arryDuck[2] = new MuteDuckClass(new MuteDuckDisplay(), new MuteDuckSound());
            arryDuck[3] = new RubberDuckClass(new RubberDuckDisplay(), new RubberDuckSound());
            arryDuck[4] = new MuteDuckClass(new MuteDuckDisplay(), new MuteDuckSound());

            foreach (SuperDuck duck in arryDuck)
            {
                duck.Sound();
                duck.Display();
            }
            int a = 3;
        }
    }
}
