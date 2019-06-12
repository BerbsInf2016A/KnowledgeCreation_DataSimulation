using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using SimulationCSVConverter.Objects;

namespace SimulationCSVConverter.Functions
{
    public class AnalysingService
    {
        public static List<Machine> AnalyseCSV(string path)
        {
            string text = File.ReadAllText(path);
            List<string> textEntries = text.Split("\n").ToList();
            textEntries.RemoveAt(0);  // Removes first line due to unnecessary header.

            List<Entry> entries = ConvertEntries(textEntries);
            List<Machine> machines = AnalyseEntries(entries);

            return machines;
        }


        private static List<Entry> ConvertEntries(List<string> textEntries)
        {
            List<Entry> entries = new List<Entry>();
            foreach (string textEntry in textEntries)
            {
                if (string.IsNullOrWhiteSpace(textEntry)) continue;

                string[] split = textEntry.Split("\"");
                Entry entry = new Entry();
                entry.MachineName = split[1];
                entry.StartTime = split[3];
                entry.EndTime = split[7];
                entry.Code = split[9];

                string[] dateSplit = split[5].Split("/");
                entry.Date = new DateTime(Convert.ToInt32(dateSplit[2]), Convert.ToInt32(dateSplit[0]), Convert.ToInt32(dateSplit[1]));

                entries.Add(entry);
            }

            return entries;
        }

        private static List<Machine> AnalyseEntries(List<Entry> entries)
        {
            List<Machine> machines = new List<Machine>();

            foreach (Entry entry in entries)
            {
                Machine machine;
                if (machines.Any(x => x.Name == entry.MachineName))
                {
                    machine = machines.First(x => x.Name == entry.MachineName);
                }
                else
                {
                    machine = new Machine();
                    machines.Add(machine);
                    machine.Name = entry.MachineName;
                }

                WorkDay workDay;
                if (machine.WorkDays.Any(x => x.Date == entry.Date))
                {
                    workDay = machine.WorkDays.First(x => x.Date == entry.Date);
                }
                else
                {
                    workDay = new WorkDay();
                    machine.WorkDays.Add(workDay);
                    workDay.Date = entry.Date;
                }

                Signal signal = new Signal();
                signal.StartTime = Convert.ToInt32(entry.StartTime);
                signal.EndTime = Convert.ToInt32(entry.EndTime);
                signal.Code = Convert.ToInt32(entry.Code);
                workDay.Signals.Add(signal);
            }

            return machines;
        }


        
    }
}
