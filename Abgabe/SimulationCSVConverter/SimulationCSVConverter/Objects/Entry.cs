using System;

namespace SimulationCSVConverter.Objects
{
    public class Entry
    {
        public string MachineName { get; set; }
        public string StartTime { get; set; }
        public DateTime Date { get; set; }
        public string EndTime { get; set; }
        public string Code { get; set; }
    }
}
