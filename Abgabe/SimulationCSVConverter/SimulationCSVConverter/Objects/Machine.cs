using System.Collections.Generic;

namespace SimulationCSVConverter.Objects
{
    public class Machine
    {
        public string Name { get; set; }
        public List<WorkDay> WorkDays { get; set; }

        public Machine()
        {
            WorkDays = new List<WorkDay>();
        }
    }
}
