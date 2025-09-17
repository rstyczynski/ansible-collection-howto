#!/usr/bin/env python3
"""
JUnit XML to HTML Report Converter

This script converts JUnit XML test reports to HTML format with a modern, responsive design.
It provides detailed test results, statistics, and visual indicators for test status.

Build with ChatGPT

Usage:
    python junit_to_html.py <input_xml_file> [output_html_file]

Example:
    python junit_to_html.py reports/verify-1758049908.148396.xml report.html
"""

import xml.etree.ElementTree as ET
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class JUnitToHTMLConverter:
    def __init__(self):
        self.css_styles = """
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f5f5f5;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header .subtitle {
                font-size: 1.2em;
                opacity: 0.9;
            }
            
            .source-info {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 15px;
                margin-top: 15px;
                border-left: 4px solid rgba(255, 255, 255, 0.3);
            }
            
            .source-info .source-label {
                font-size: 0.9em;
                opacity: 0.8;
                margin-bottom: 5px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .source-info .source-path {
                font-family: 'Courier New', monospace;
                font-size: 0.95em;
                word-break: break-all;
                background: rgba(0, 0, 0, 0.2);
                padding: 8px 12px;
                border-radius: 4px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .stat-card {
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                text-align: center;
                transition: transform 0.2s;
            }
            
            .stat-card:hover {
                transform: translateY(-2px);
            }
            
            .stat-number {
                font-size: 2.5em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            .stat-label {
                color: #666;
                font-size: 1.1em;
            }
            
            .tests-total { color: #3498db; }
            .tests-passed { color: #27ae60; }
            .tests-failed { color: #e74c3c; }
            .tests-skipped { color: #f39c12; }
            .tests-errors { color: #9b59b6; }
            
            .test-results {
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }
            
            .test-results-header {
                background: #34495e;
                color: white;
                padding: 20px;
                font-size: 1.3em;
                font-weight: bold;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .bulk-actions {
                display: flex;
                gap: 10px;
            }
            
            .bulk-action-btn {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 0.9em;
                transition: background-color 0.2s;
            }
            
            .bulk-action-btn:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            
            .test-case {
                border-bottom: 1px solid #eee;
                padding: 20px;
                transition: background-color 0.2s;
            }
            
            .test-case:hover {
                background-color: #f8f9fa;
            }
            
            .test-case:last-child {
                border-bottom: none;
            }
            
            .test-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                cursor: pointer;
                user-select: none;
            }
            
            .test-header:hover {
                background-color: rgba(0, 0, 0, 0.02);
                border-radius: 5px;
                padding: 5px;
                margin: -5px;
            }
            
            .test-header-left {
                display: flex;
                align-items: center;
                flex: 1;
            }
            
            .toggle-button {
                background: none;
                border: none;
                font-size: 1.2em;
                margin-right: 10px;
                cursor: pointer;
                color: #666;
                transition: transform 0.2s, color 0.2s;
                padding: 5px;
                border-radius: 3px;
            }
            
            .toggle-button:hover {
                color: #333;
                background-color: rgba(0, 0, 0, 0.05);
            }
            
            .toggle-button.expanded {
                transform: rotate(90deg);
                color: #007bff;
            }
            
            .test-name {
                font-weight: bold;
                font-size: 1.1em;
                color: #2c3e50;
            }
            
            .test-status {
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: bold;
                text-transform: uppercase;
            }
            
            .status-passed {
                background-color: #d4edda;
                color: #155724;
            }
            
            .status-failed {
                background-color: #f8d7da;
                color: #721c24;
            }
            
            .status-skipped {
                background-color: #fff3cd;
                color: #856404;
            }
            
            .status-error {
                background-color: #f8d7da;
                color: #721c24;
            }
            
            .test-details {
                margin-top: 15px;
                overflow: hidden;
                transition: max-height 0.3s ease-out, opacity 0.3s ease-out;
                max-height: 0;
                opacity: 0;
            }
            
            .test-details.expanded {
                max-height: 2000px;
                opacity: 1;
            }
            
            .test-detail-row {
                display: flex;
                margin-bottom: 8px;
            }
            
            .test-detail-label {
                font-weight: bold;
                min-width: 120px;
                color: #555;
            }
            
            .test-detail-value {
                flex: 1;
                word-break: break-all;
            }
            
            .system-out {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 15px;
                margin-top: 10px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
                white-space: pre-wrap;
                max-height: 200px;
                overflow-y: auto;
            }
            
            .skipped-reason {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
                color: #856404;
            }
            
            .error-message {
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
                color: #721c24;
            }
            
            .footer {
                text-align: center;
                margin-top: 40px;
                padding: 20px;
                color: #666;
                border-top: 1px solid #eee;
            }
            
            @media (max-width: 768px) {
                .container {
                    padding: 10px;
                }
                
                .header h1 {
                    font-size: 2em;
                }
                
                .stats-grid {
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                }
                
                .test-header {
                    flex-direction: column;
                    align-items: flex-start;
                }
                
                .test-header-left {
                    width: 100%;
                    margin-bottom: 10px;
                }
                
                .test-status {
                    margin-top: 10px;
                }
                
                .test-results-header {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 15px;
                }
                
                .bulk-actions {
                    width: 100%;
                    justify-content: flex-start;
                }
            }
        </style>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Initialize all test cases as collapsed
                const testCases = document.querySelectorAll('.test-case');
                testCases.forEach((testCase, index) => {
                    const toggleBtn = testCase.querySelector('.toggle-button');
                    const details = testCase.querySelector('.test-details');
                    
                    // Set initial state (collapsed)
                    toggleBtn.textContent = '▶';
                    details.classList.remove('expanded');
                    
                    // Add click event listener
                    testCase.querySelector('.test-header').addEventListener('click', function() {
                        toggleTestDetails(toggleBtn, details);
                    });
                });
                
                // Bulk action buttons
                const expandAllBtn = document.getElementById('expand-all');
                const collapseAllBtn = document.getElementById('collapse-all');
                
                if (expandAllBtn) {
                    expandAllBtn.addEventListener('click', function() {
                        testCases.forEach(testCase => {
                            const toggleBtn = testCase.querySelector('.toggle-button');
                            const details = testCase.querySelector('.test-details');
                            if (!details.classList.contains('expanded')) {
                                toggleTestDetails(toggleBtn, details);
                            }
                        });
                    });
                }
                
                if (collapseAllBtn) {
                    collapseAllBtn.addEventListener('click', function() {
                        testCases.forEach(testCase => {
                            const toggleBtn = testCase.querySelector('.toggle-button');
                            const details = testCase.querySelector('.test-details');
                            if (details.classList.contains('expanded')) {
                                toggleTestDetails(toggleBtn, details);
                            }
                        });
                    });
                }
                
                // Keyboard navigation
                document.addEventListener('keydown', function(e) {
                    if (e.ctrlKey || e.metaKey) {
                        if (e.key === 'a') {
                            e.preventDefault();
                            const expandAllBtn = document.getElementById('expand-all');
                            if (expandAllBtn) expandAllBtn.click();
                        } else if (e.key === 'd') {
                            e.preventDefault();
                            const collapseAllBtn = document.getElementById('collapse-all');
                            if (collapseAllBtn) collapseAllBtn.click();
                        }
                    }
                });
            });
            
            function toggleTestDetails(toggleBtn, details) {
                const isExpanded = details.classList.contains('expanded');
                
                if (isExpanded) {
                    // Collapse
                    toggleBtn.textContent = '▶';
                    toggleBtn.classList.remove('expanded');
                    details.classList.remove('expanded');
                } else {
                    // Expand
                    toggleBtn.textContent = '▼';
                    toggleBtn.classList.add('expanded');
                    details.classList.add('expanded');
                }
            }
        </script>
        """

    def parse_junit_xml(self, xml_file: str) -> Dict:
        """Parse JUnit XML file and extract test data."""
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Extract testsuite data
            testsuite = root.find('testsuite')
            if testsuite is None:
                raise ValueError("No testsuite found in XML")
            
            # Parse attributes
            suite_data = {
                'name': testsuite.get('name', 'Unknown'),
                'tests': int(testsuite.get('tests', 0)),
                'disabled': int(testsuite.get('disabled', 0)),
                'errors': int(testsuite.get('errors', 0)),
                'failures': int(testsuite.get('failures', 0)),
                'skipped': int(testsuite.get('skipped', 0)),
                'time': float(testsuite.get('time', 0)),
                'test_cases': []
            }
            
            # Calculate passed tests
            suite_data['passed'] = suite_data['tests'] - suite_data['errors'] - suite_data['failures'] - suite_data['skipped']
            
            # Parse test cases
            for testcase in testsuite.findall('testcase'):
                case_data = {
                    'name': testcase.get('name', 'Unknown'),
                    'classname': testcase.get('classname', ''),
                    'time': float(testcase.get('time', 0)),
                    'status': 'passed',
                    'system_out': '',
                    'skipped': '',
                    'error': '',
                    'failure': ''
                }
                
                # Check for different test outcomes
                if testcase.find('skipped') is not None:
                    case_data['status'] = 'skipped'
                    case_data['skipped'] = testcase.find('skipped').text or 'Skipped'
                elif testcase.find('error') is not None:
                    case_data['status'] = 'error'
                    case_data['error'] = testcase.find('error').text or 'Error occurred'
                elif testcase.find('failure') is not None:
                    case_data['status'] = 'failed'
                    case_data['failure'] = testcase.find('failure').text or 'Test failed'
                
                # Get system output
                system_out = testcase.find('system-out')
                if system_out is not None and system_out.text:
                    case_data['system_out'] = system_out.text.strip()
                
                suite_data['test_cases'].append(case_data)
            
            return suite_data
            
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML file: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing XML: {e}")

    def format_time(self, seconds: float) -> str:
        """Format time in a human-readable format."""
        if seconds < 1:
            return f"{seconds * 1000:.1f} ms"
        elif seconds < 60:
            return f"{seconds:.2f} s"
        else:
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds:.1f}s"

    def clean_test_name(self, test_name: str) -> str:
        """Clean up test name to make it shorter and more readable."""
        if not test_name:
            return "Unknown Test"
        
        # Remove common prefixes and suffixes
        cleaned = test_name
        
        # Remove host information like [centos], [ubuntu]
        import re
        cleaned = re.sub(r'\[[^\]]+\]\s*', '', cleaned)
        
        # Remove "Verify:" prefix
        cleaned = re.sub(r'^Verify:\s*', '', cleaned, flags=re.IGNORECASE)
        
        # Remove "TEST_CASE:" prefix
        cleaned = re.sub(r'^TEST_CASE:\s*', '', cleaned, flags=re.IGNORECASE)
        
        # Remove long parameter lists in parentheses
        cleaned = re.sub(r'\s*\([^)]{50,}\)', '', cleaned)
        
        # Remove long parameter lists after commas
        if ',' in cleaned:
            parts = cleaned.split(',')
            if len(parts) > 1:
                # Keep only the first meaningful part
                first_part = parts[0].strip()
                # Remove common suffixes from first part
                first_part = re.sub(r'\s+(that=|fail_msg=|success_msg=).*', '', first_part)
                cleaned = first_part
        
        # Remove common verbose patterns
        cleaned = re.sub(r'\s+(that=|fail_msg=|success_msg=).*', '', cleaned)
        cleaned = re.sub(r'\s+port=\d+.*', '', cleaned)
        cleaned = re.sub(r'\s+host=.*', '', cleaned)
        cleaned = re.sub(r'\s+state=.*', '', cleaned)
        cleaned = re.sub(r'\s+timeout=\d+.*', '', cleaned)
        
        # Clean up extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # If the name is still too long, truncate it
        if len(cleaned) > 60:
            cleaned = cleaned[:57] + "..."
        
        return cleaned if cleaned else "Test Case"

    def generate_html(self, test_data: Dict, output_file: str, source_file: str = "") -> None:
        """Generate HTML report from test data."""
        # Build source info section
        source_section = ""
        if source_file:
            source_section = f"""
            <div class="source-info">
                <div class="source-label">Source File</div>
                <div class="source-path">{self.escape_html(source_file)}</div>
            </div>"""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report - {test_data['name']}</title>
    {self.css_styles}
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Test Report</h1>
            <div class="subtitle">
                {test_data['name']} • Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>{source_section}
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number tests-total">{test_data['tests']}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number tests-passed">{test_data['passed']}</div>
                <div class="stat-label">Passed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number tests-failed">{test_data['failures']}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number tests-errors">{test_data['errors']}</div>
                <div class="stat-label">Errors</div>
            </div>
            <div class="stat-card">
                <div class="stat-number tests-skipped">{test_data['skipped']}</div>
                <div class="stat-label">Skipped</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{self.format_time(test_data['time'])}</div>
                <div class="stat-label">Total Time</div>
            </div>
        </div>
        
        <div class="test-results">
            <div class="test-results-header">
                <div>📋 Test Cases ({len(test_data['test_cases'])})</div>
                <div class="bulk-actions">
                    <button class="bulk-action-btn" id="expand-all">Expand All</button>
                    <button class="bulk-action-btn" id="collapse-all">Collapse All</button>
                </div>
            </div>
"""
        
        # Generate test case details
        for i, test_case in enumerate(test_data['test_cases'], 1):
            status_class = f"status-{test_case['status']}"
            status_text = test_case['status'].upper()
            cleaned_name = self.clean_test_name(test_case['name'])
            
            html_content += f"""
            <div class="test-case">
                <div class="test-header">
                    <div class="test-header-left">
                        <button class="toggle-button" aria-label="Toggle test details">▶</button>
                        <div class="test-name">
                            {i}. {self.escape_html(cleaned_name)}
                        </div>
                    </div>
                    <div class="test-status {status_class}">
                        {status_text}
                    </div>
                </div>
                
                <div class="test-details">
                    <div class="test-detail-row">
                        <div class="test-detail-label">Full Name:</div>
                        <div class="test-detail-value">{self.escape_html(test_case['name'])}</div>
                    </div>
                    <div class="test-detail-row">
                        <div class="test-detail-label">Duration:</div>
                        <div class="test-detail-value">{self.format_time(test_case['time'])}</div>
                    </div>
                    <div class="test-detail-row">
                        <div class="test-detail-label">Class:</div>
                        <div class="test-detail-value">{self.escape_html(test_case['classname'])}</div>
                    </div>
"""
            
            # Add status-specific content
            if test_case['status'] == 'skipped' and test_case['skipped']:
                html_content += f"""
                    <div class="skipped-reason">
                        <strong>Skip Reason:</strong> {self.escape_html(test_case['skipped'])}
                    </div>
"""
            elif test_case['status'] == 'error' and test_case['error']:
                html_content += f"""
                    <div class="error-message">
                        <strong>Error:</strong> {self.escape_html(test_case['error'])}
                    </div>
"""
            elif test_case['status'] == 'failed' and test_case['failure']:
                html_content += f"""
                    <div class="error-message">
                        <strong>Failure:</strong> {self.escape_html(test_case['failure'])}
                    </div>
"""
            
            # Add system output if available
            if test_case['system_out']:
                html_content += f"""
                    <div class="system-out">
                        <strong>Output:</strong>
{self.escape_html(test_case['system_out'])}
                    </div>
"""
            
            html_content += """
                </div>
            </div>
"""
        
        # Close HTML
        html_content += f"""
        </div>
        
        <div class="footer">
            <p>Generated by JUnit to HTML Converter • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        if not text:
            return ''
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))

    def convert(self, input_file: str, output_file: Optional[str] = None) -> str:
        """Convert JUnit XML to HTML."""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        if output_file is None:
            # Generate output file next to the source XML file
            input_dir = os.path.dirname(input_file)
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(input_dir, f"{base_name}_report.html")
        else:
            # If output file is specified without a directory, place it next to the source file
            if not os.path.dirname(output_file):
                input_dir = os.path.dirname(input_file)
                output_file = os.path.join(input_dir, output_file)
        
        print(f"Parsing JUnit XML: {input_file}")
        test_data = self.parse_junit_xml(input_file)
        
        print(f"Generating HTML report: {output_file}")
        self.generate_html(test_data, output_file, input_file)
        
        print(f"✅ Report generated successfully!")
        print(f"📊 Summary: {test_data['tests']} tests, {test_data['passed']} passed, {test_data['failures']} failed, {test_data['errors']} errors, {test_data['skipped']} skipped")
        
        return output_file


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python junit_to_html.py <input_xml_file> [output_html_file]")
        print("\nExample:")
        print("  python junit_to_html.py reports/verify-1758049908.148396.xml report.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        converter = JUnitToHTMLConverter()
        result_file = converter.convert(input_file, output_file)
        print(f"\n🌐 Open the report in your browser: file://{os.path.abspath(result_file)}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
