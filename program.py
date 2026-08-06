# faculty_research.py

import json
import os

# Sample data representing university project details as dictionaries
faculty_data = [
    {
        "Faculty ID": "F001",
        "Faculty Name": "Dr. Alice Smith",
        "Department": "Computer Science",
        "Number of Publications": 25,
        "H-index": 12,
        "Project Budget Requested": 120000,
        "Industry Collaboration Score": 85,
    },
    {
        "Faculty ID": "F002",
        "Faculty Name": "Dr. Bob Jones",
        "Department": "Mechanical Engineering",
        "Number of Publications": 10,
        "H-index": 5,
        "Project Budget Requested": 90000,
        "Industry Collaboration Score": 40,
    },
    {
        "Faculty ID": "F003",
        "Faculty Name": "Dr. Carol White",
        "Department": "Computer Science",
        "Number of Publications": 35,
        "H-index": 20,
        "Project Budget Requested": 150000,
        "Industry Collaboration Score": 95,
    },
    {
        "Faculty ID": "F004",
        "Faculty Name": "Dr. David Brown",
        "Department": "Electrical Engineering",
        "Number of Publications": 5,
        "H-index": 2,
        "Project Budget Requested": -5000,  # Invalid budget for testing
        "Industry Collaboration Score": 20,
    },
]


def validate_and_process_data(data):
  processed = []
  for faculty in data:
    try:
      # 10. Handle invalid budgets
      budget = faculty["Project Budget Requested"]
      if budget < 0:
        raise ValueError(
            f"Invalid budget (${budget}) for {faculty['Faculty Name']}. Setting"
            " to $0."
        )
    except ValueError as e:
      print(f"Warning: {e}")
      budget = 0

    # 1. Calculate research score
    pubs = faculty["Number of Publications"]
    h_index = faculty["H-index"]
    collab = faculty["Industry Collaboration Score"]

    research_score = (0.4 * pubs) + (0.3 * h_index) + (0.3 * collab)

    # 2. Allocate grants based on research score (e.g., $4,000 per score point)
    allocated_grant = research_score * 4000

    faculty_record = {
        "Faculty ID": faculty["Faculty ID"],
        "Faculty Name": faculty["Faculty Name"],
        "Department": faculty["Department"],
        "Research Score": round(research_score, 2),
        "Allocated Grant": round(allocated_grant, 2),
        "Project Budget Requested": budget,
    }
    processed.append(faculty_record)
  return processed


def main():
  records = validate_and_process_data(faculty_data)

  print("=== 3. Faculty Receiving Grants Above $100,000 ===")
  high_grants = [r for r in records if r["Allocated Grant"] > 100000]
  for h in high_grants:
    print(
        f"- {h['Faculty Name']} ({h['Department']}):"
        f" ${h['Allocated Grant']}"
    )

  print("\n=== 4. Department Receiving Maximum Funding ===")
  dept_funding = {}
  for r in records:
    dept = r["Department"]
    dept_funding[dept] = dept_funding.get(dept, 0.0) + r["Allocated Grant"]

  max_dept = max(dept_funding, key=dept_funding.get)
  print(
      f"Department: {max_dept} with total funding of ${dept_funding[max_dept]}"
  )

  print("\n=== 5. Rank Faculty Members ===")
  # Sort by Research Score descending
  ranked_faculty = sorted(
      records, key=lambda x: x["Research Score"], reverse=True
  )
  for rank, faculty in enumerate(ranked_faculty, start=1):
    print(
        f"Rank {rank}: {faculty['Faculty Name']} (Score:"
        f" {faculty['Research Score']})"
    )

  print("\n=== 6. Calculate Average Research Score ===")
  avg_score = sum(f["Research Score"] for f in records) / len(records)
  print(f"Average Research Score: {round(avg_score, 2)}")

  print("\n=== 7. Identify Top Performer ===")
  top_performer = ranked_faculty[0]
  print(
      f"Top Performer: {top_performer['Faculty Name']} from"
      f" {top_performer['Department']} with score"
      f" {top_performer['Research Score']}"
  )

  # 8. Save rankings to a file
  filename = "rankings.json"
  with open(filename, "w") as f:
    json.dump(ranked_faculty, f, indent=4)
  print(f"\n=== 8. Rankings successfully saved to {filename} ===")

  # 9. Read the rankings back
  print("\n=== 9. Reading Rankings Back from File ===")
  if os.path.exists(filename):
    with open(filename, "r") as f:
      read_data = json.load(f)
      for entry in read_data:
        print(
            f"Read from file -> {entry['Faculty Name']}: Score"
            f" {entry['Research Score']}"
        )


if __name__ == "__main__":
  main()
