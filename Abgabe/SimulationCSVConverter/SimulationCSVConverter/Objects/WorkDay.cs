using System;
using System.Collections.Generic;

namespace SimulationCSVConverter.Objects
{
    public class WorkDay
    {
        public DateTime Date { get; set; }
        public List<Signal> Signals { get; set; }

        public WorkDay()
        {
            Signals = new List<Signal>();
        }
    }
}
