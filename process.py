# machine_analysis.py

import json
import os

# Sample data representing machine details as dictionaries
machine_data = [
    {
        "Machine ID": "M001",
        "Plant Name": "Plant Alpha",
        "Operating Hours": 200,
        "Downtime": 10,
        "Energy Consumption": 1500,
        "Units Produced": 5000,
        "Maintenance Cost": 1200.0,
    },
    {
        "Machine ID": "M002",
        "Plant Name": "Plant Alpha",
        "Operating Hours": 200,
        "Downtime": 50,  # High downtime
        "Energy Consumption": 1800,
        "Units Produced": 2000,
        "Maintenance Cost": 3500.0,
    },
    {
        "Machine ID": "M003",
        "Plant Name": "Plant Beta",
        "Operating Hours": 180,
        "Downtime": 5,
        "Energy Consumption": 1200,
        "Units Produced": 4800,
        "Maintenance Cost": 800.0,
    },
    {
        "Machine ID": "M004",
        "Plant Name": "Plant Beta",
        "Operating Hours": 220,
        "Downtime": 0,  # Handled to avoid division by zero
        "Energy Consumption": 2000,
        "Units Produced": 6000,
        "Maintenance Cost": 1500.0,
    },
]


def process_machine_data(data):
  processed = []
  for machine in data:
    op_hours = machine["Operating Hours"]
    downtime = machine["Downtime"]
    units = machine["Units Produced"]
    energy = machine["Energy Consumption"]
    maint_cost = machine["Maintenance Cost"]

    # 1. Calculate machine efficiency (Units Produced per active hour)
    active_hours = op_hours - downtime
    if active_hours <= 0:
      active_hours = 1  # Prevent division by zero

    efficiency = units / active_hours

    # 2. Calculate production cost per unit (Assuming standard energy cost + maintenance proportion)
    total_cost = energy * 0.15 + maint_cost
    cost_per_unit = total_cost / units if units > 0 else 0

    machine_record = {
        "Machine ID": machine["Machine ID"],
        "Plant Name": machine["Plant Name"],
        "Operating Hours": op_hours,
        "Downtime": downtime,
        "Efficiency": round(efficiency, 2),
        "Cost Per Unit": round(cost_per_unit, 2),
        "Maintenance Cost": maint_cost,
    }
    processed.append(machine_record)
  return processed


def main():
  records = process_machine_data(machine_data)

  print("=== 3. Inefficient Machines (Efficiency < 25 units/hr) ===")
  inefficient = [r for r in records if r["Efficiency"] < 25.0]
  for m in inefficient:
    print(
        f"- {m['Machine ID']} ({m['Plant Name']}): Efficiency"
        f" {m['Efficiency']}"
    )

  print("\n=== 4. Machine with Highest Maintenance Cost ===")
  highest_maint = max(records, key=lambda x: x["Maintenance Cost"])
  print(
      f"Machine ID: {highest_maint['Machine ID']} from"
      f" {highest_maint['Plant Name']} with cost"
      f" ${highest_maint['Maintenance Cost']}"
  )

  print("\n=== 5. Plant-wise Efficiency ===")
  plant_stats = {}
  for r in records:
    plant = r["Plant Name"]
    if plant not in plant_stats:
      plant_stats[plant] = {"total_eff": 0.0, "count": 0}
    plant_stats[plant]["total_eff"] += r["Efficiency"]
    plant_stats[plant]["count"] += 1

  for plant, stats in plant_stats.items():
    avg_plant_eff = stats["total_eff"] / stats["count"]
    print(f"Plant: {plant} | Average Efficiency: {round(avg_plant_eff, 2)}")

  print("\n=== 6. Machines Requiring Preventive Maintenance ===")
  # Criteria: High downtime (> 20 hours) or High Maintenance Cost (> 2000)
  preventive_list = [
      r
      for r in records
      if r["Downtime"] > 20 or r["Maintenance Cost"] > 2000.0
  ]
  for p in preventive_list:
    print(
        f"- {p['Machine ID']} ({p['Plant Name']}) requires attention due to"
        f" downtime ({p['Downtime']} hrs) or cost (${p['Maintenance Cost']})"
    )

  print("\n=== 7. Sort Machines by Efficiency (Descending) ===")
  sorted_machines = sorted(records, key=lambda x: x["Efficiency"], reverse=True)
  for rank, machine in enumerate(sorted_machines, start=1):
    print(
        f"Rank {rank}: {machine['Machine ID']} - Efficiency:"
        f" {machine['Efficiency']}"
    )

  # 8. & 9. Generate maintenance report and save to file
  filename = "maintenance_report.json"
  report = {
      "sorted_machines": sorted_machines,
      "preventive_maintenance_required": preventive_list,
  }

  with open(filename, "w") as f:
    json.dump(report, f, indent=4)
  print(f"\n=== 8 & 9. Maintenance report successfully saved to {filename} ===")

  # 10. Read the report back
  print("\n=== 10. Reading Maintenance Report Back from File ===")
  if os.path.exists(filename):
    with open(filename, "r") as f:
      loaded_report = json.load(f)
      print(
          "Successfully read report. Total machines logged:"
          f" {len(loaded_report['sorted_machines'])}"
      )
      for entry in loaded_report["sorted_machines"]:
        print(
            f"Loaded -> Machine: {entry['Machine ID']} | Cost Per Unit:"
            f" ${entry['Cost Per Unit']}"
        )


if __name__ == "__main__":
  main()
