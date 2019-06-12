using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SimulationCSVConverter.Objects;

namespace SimulationCSVConverter.Functions
{
    public class CSVConverterService
    {
        public static bool ConvertCSV(List<Machine> machines, string directory, int interval, bool onlyAcceptBinaryValue, int[] binaryAcceptValues, bool useShortNotationForm)
        {
            foreach (Machine machine in machines)
            {
                new Task(() => ConvertMachine(machine, directory, interval, onlyAcceptBinaryValue, binaryAcceptValues, useShortNotationForm)).Start();
            }

            return true;
        }

        private static void ConvertMachine(Machine machine, string directory, int interval, bool onlyAcceptBinaryValue, int[] binaryAcceptValues, bool useShortNotationForm)
        {
            foreach (WorkDay machineWorkDay in machine.WorkDays)
            {
                string text = CreateHeader(machine, machineWorkDay, interval);
                text += ConvertMachineWorkDayValues(machineWorkDay, interval, onlyAcceptBinaryValue, binaryAcceptValues, useShortNotationForm);
                CreateFile(text, directory, machine, machineWorkDay);
            }
        }

        private static string CreateHeader(Machine machine, WorkDay workDay, int interval)
        {
            return $"$Machine,{machine.Name},Start,{workDay.Date:yyyy-MM-dd-HH-mm-ss},End,{workDay.Date:yyyy-MM-dd-23-59-59},Interval,{interval}ms$\n";
        }

        private static string ConvertMachineWorkDayValues(WorkDay machineWorkDay, int interval, bool onlyAcceptBinaryValue, int[] binaryAcceptValues, bool useShortNotationForm)
        {
            interval = interval / 1000;
            List<int> intervals = new List<int>();
            int secondsDay = 60 * 60 * 24;
            for (int i = 0; i < secondsDay; i += interval)
            {
                intervals.Add(i);
            }

            List<int> codes = new List<int>();
            bool found;

            foreach (int i in intervals)
            {
                found = false;
                foreach (Signal signal in machineWorkDay.Signals)
                {
                    if (!found && signal.StartTime <= i && signal.EndTime > i)
                    {
                        found = true;
                        if (onlyAcceptBinaryValue)
                        {
                            if (binaryAcceptValues.Contains(signal.Code)) codes.Add(0);
                            else codes.Add(1);
                        }
                        else
                        {
                            codes.Add(signal.Code);
                        }
                    }
                }

                if (!found)
                {
                    if (onlyAcceptBinaryValue) codes.Add(1);
                    else codes.Add(0);
                }
            }

            return ConvertNumberListToString(codes, useShortNotationForm);
        }

        private static string ConvertNumberListToString(List<int> codes, bool useShortNotationForm)
        {
            StringBuilder sb = new StringBuilder();

            if (useShortNotationForm)
            {
                int lastCode = 0;
                int codeCount = 0;

                foreach (int code in codes)
                {
                    if (lastCode == code)
                    {
                        codeCount++;
                    }
                    else
                    {
                        if (codeCount != 0) sb.Append($"{codeCount}|{lastCode},");
                        lastCode = code;
                        codeCount = 1;
                    }
                }

                if (codeCount != 0) sb.Append($"{codeCount}|{lastCode},");
            }
            else
            {
               sb.Append(string.Join(",", codes));
            }

            if (sb.Length > 0) sb.Remove(sb.Length - 1, 1);

            return sb.ToString();
        }

        private static void CreateFile(string text, string directory, Machine machine, WorkDay machineWorkDay)
        {
            string filename = $"{directory}/ConvertedCSV{DateTime.Now:ddMM}/{machine.Name}_{machineWorkDay.Date:yyyy-MM-dd}.csv";
            if (!Directory.Exists($"{directory}/ConvertedCSV{DateTime.Now:ddMM}")) Directory.CreateDirectory($"{directory}/ConvertedCSV{DateTime.Now:ddMM}");
            File.WriteAllText(filename, text);
        }
    }
}
