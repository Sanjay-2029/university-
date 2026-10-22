<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Citizen Road Reporting Portal</title>
    <style>
        :root {
            --primary: #2563eb;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --border: #e2e8f0;
        }
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.5;
            margin: 0;
            padding: 2rem;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        h1, h2 {
            color: #0f172a;
        }
        
        /* Summary Cards Dashboard */
        .summary-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .summary-card {
            background: var(--card-bg);
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border: 1px solid var(--border);
            text-align: center;
        }
        .summary-card h3 {
            margin: 0;
            font-size: 0.875rem;
            text-transform: uppercase;
            color: #64748b;
        }
        .summary-card .count {
            font-size: 1.75rem;
            font-weight: 700;
            margin-top: 0.5rem;
        }

        /* Filter Section */
        .filter-section {
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        select {
            padding: 0.5rem 1rem;
            font-size: 1rem;
            border-radius: 6px;
            border: 1px solid var(--border);
            background-color: var(--card-bg);
            cursor: pointer;
        }

        /* Table Styling */
        table {
            width: 100%;
            border-collapse: collapse;
            background: var(--card-bg);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border: 1px solid var(--border);
        }
        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        th {
            background-color: #f1f5f9;
            font-weight: 600;
        }
        tr:last-child td {
            border-bottom: none;
        }

        /* Status Badges */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        .status-resolved { background-color: #dcfce7; color: #15803d; }
        .status-pending { background-color: #fef9c3; color: #a16207; }
        .status-in-progress { background-color: #dbeafe; color: #1d4ed8; }
    </style>
</head>
<body>

    <div class="container">
        <h1>Citizen Road Reporting Portal</h1>

        <!-- Complaint Status Summary -->
        <h2>Complaint Status Summary</h2>
        <div class="summary-container">
            <div class="summary-card">
                <h3>Total Complaints</h3>
                <div class="count" id="total-count">0</div>
            </div>
            <div class="summary-card">
                <h3>Resolved</h3>
                <div class="count" id="resolved-count" style="color: #15803d;">0</div>
            </div>
            <div class="summary-card">
                <h3>In Progress</h3>
                <div class="count" id="progress-count" style="color: #1d4ed8;">0</div>
            </div>
            <div class="summary-card">
                <h3>Pending</h3>
                <div class="count" id="pending-count" style="color: #a16207;">0</div>
            </div>
        </div>

        <!-- Filter Controls -->
        <div class="filter-section">
            <label for="categoryFilter"><strong>Filter by Category:</strong></label>
            <select id="categoryFilter" onchange="filterComplaints()">
                <option value="all">All Categories</option>
                <option value="pothole">Pothole</option>
                <option value="damaged streetlight">Damaged Streetlight</option>
                <option value="waterlogging">Waterlogging</option>
            </select>
        </div>

        <!-- Complaints Table -->
        <table id="complaintsTable">
            <thead>
                <tr>
                    <th>Complaint ID</th>
                    <th>Category</th>
                    <th>Affected Location</th>
                    <th>Report Date</th>
                    <th>Resolution Status</th>
                </tr>
            </thead>
            <tbody id="complaintsBody">
                <!-- Rendered dynamically by JavaScript -->
            </tbody>
        </table>
    </div>

    <script>
        // Sample Data representing the 5 road complaints
        const complaints = [
            { id: "CMP-001", category: "pothole", location: "102 Main Street, Downtown", date: "2026-10-15", status: "Resolved" },
            { id: "CMP-002", category: "damaged streetlight", location: "Oak Avenue & 4th Cross", date: "2026-10-18", status: "Pending" },
            { id: "CMP-003", category: "waterlogging", location: "Subway Underpass, Sector 5", date: "2026-10-19", status: "In Progress" },
            { id: "CMP-004", category: "pothole", location: "By-pass Road near Highway Entry", date: "2026-10-20", status: "Pending" },
            { id: "CMP-005", category: "damaged streetlight", location: "Riverview Residential Lane", date: "2026-10-21", status: "Resolved" }
        ];

        // Function to assign CSS classes based on status
        function getStatusClass(status) {
            switch(status.toLowerCase()) {
                case 'resolved': return 'status-resolved';
                case 'in progress': return 'status-in-progress';
                default: return 'status-pending';
            }
        }

        // Calculates and renders metrics dynamically based on visible data or full dataset
        function updateSummaryDashboard() {
            const totals = complaints.reduce((acc, curr) => {
                acc.total++;
                if (curr.status === "Resolved") acc.resolved++;
                else if (curr.status === "In Progress") acc.progress++;
                else if (curr.status === "Pending") acc.pending++;
                return acc;
            }, { total: 0, resolved: 0, progress: 0, pending: 0 });

            document.getElementById('total-count').innerText = totals.total;
            document.getElementById('resolved-count').innerText = totals.resolved;
            document.getElementById('progress-count').innerText = totals.progress;
            document.getElementById('pending-count').innerText = totals.pending;
        }

        // Render rows dynamically into the DOM
        function renderTable(data) {
            const tbody = document.getElementById('complaintsBody');
            tbody.innerHTML = '';

            data.forEach(complaint => {
                const row = `
                    <tr>
                        <td><strong>${complaint.id}</strong></td>
                        <td style="text-transform: capitalize;">${complaint.category}</td>
                        <td>${complaint.location}</td>
                        <td>${complaint.date}</td>
                        <td><span class="badge ${getStatusClass(complaint.status)}">${complaint.status}</span></td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        }

        // Filter functionality triggering on dropdown selection change
        function filterComplaints() {
            const selectedValue = document.getElementById('categoryFilter').value;
            
            if (selectedValue === 'all') {
                renderTable(complaints);
            } else {
                const filteredData = complaints.filter(c => c.category === selectedValue);
                renderTable(filteredData);
            }
        }

        // Global initialization
        window.onload = function() {
            renderTable(complaints);
            updateSummaryDashboard();
        };
    </script>
</body>
</html>
