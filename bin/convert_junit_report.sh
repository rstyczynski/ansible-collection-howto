#!/bin/bash

# JUnit XML to HTML Report Converter Script
# This script provides a convenient way to convert JUnit XML reports to HTML format

# Build with ChatGPT

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONVERTER_SCRIPT="$SCRIPT_DIR/junit_to_html.py"

# Function to display usage
usage() {
    echo -e "${BLUE}JUnit XML to HTML Report Converter${NC}"
    echo ""
    echo "Usage: $0 <input_xml_file> [output_html_file]"
    echo ""
    echo "Arguments:"
    echo "  input_xml_file    Path to the JUnit XML report file"
    echo "  output_html_file  Optional output HTML file path (default: auto-generated)"
    echo ""
    echo "Examples:"
    echo "  $0 reports/verify-1758049908.148396.xml"
    echo "  $0 reports/verify-1758049908.148396.xml my_report.html"
    echo "  $0 collections/ansible_collections/myorg/unix/roles/apache/molecule/junit/reports/verify-1758049908.148396.xml"
    echo ""
    echo "Features:"
    echo "  • Modern, responsive HTML design"
    echo "  • Detailed test statistics and results"
    echo "  • Color-coded test status indicators"
    echo "  • Expandable test case details"
    echo "  • Mobile-friendly interface"
}

# Function to check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        if ! command -v python &> /dev/null; then
            echo -e "${RED}Error: Python is not installed or not in PATH${NC}"
            exit 1
        else
            PYTHON_CMD="python"
        fi
    else
        PYTHON_CMD="python3"
    fi
}

# Function to check if converter script exists
check_converter() {
    if [[ ! -f "$CONVERTER_SCRIPT" ]]; then
        echo -e "${RED}Error: Converter script not found at $CONVERTER_SCRIPT${NC}"
        exit 1
    fi
}

# Function to validate input file
validate_input() {
    local input_file="$1"
    
    if [[ ! -f "$input_file" ]]; then
        echo -e "${RED}Error: Input file '$input_file' does not exist${NC}"
        exit 1
    fi
    
    if [[ ! "$input_file" =~ \.xml$ ]]; then
        echo -e "${YELLOW}Warning: Input file '$input_file' does not have .xml extension${NC}"
    fi
}

# Function to open HTML file in browser (macOS)
open_in_browser() {
    local html_file="$1"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${GREEN}Opening report in default browser...${NC}"
        open "$html_file"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v xdg-open &> /dev/null; then
            echo -e "${GREEN}Opening report in default browser...${NC}"
            xdg-open "$html_file"
        fi
    fi
}

# Main function
main() {
    # Check arguments
    if [[ $# -eq 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
        usage
        exit 0
    fi
    
    local input_file="$1"
    local output_file="$2"
    
    echo -e "${BLUE}🧪 JUnit XML to HTML Report Converter${NC}"
    echo ""
    
    # Validate environment
    check_python
    check_converter
    validate_input "$input_file"
    
    echo -e "${YELLOW}Converting JUnit XML report to HTML...${NC}"
    echo "Input:  $input_file"
    if [[ -n "$output_file" ]]; then
        echo "Output: $output_file"
    else
        echo "Output: auto-generated"
    fi
    echo ""
    
    # Run the converter
    if [[ -n "$output_file" ]]; then
        "$PYTHON_CMD" "$CONVERTER_SCRIPT" "$input_file" "$output_file"
    else
        "$PYTHON_CMD" "$CONVERTER_SCRIPT" "$input_file"
    fi
    
    # Get the actual output file name
    if [[ -n "$output_file" ]]; then
        # Check if output file has a directory path
        if [[ "$output_file" == */* ]]; then
            final_output="$output_file"
        else
            # Place custom filename next to the source XML file
            input_dir=$(dirname "$input_file")
            final_output="$input_dir/$output_file"
        fi
    else
        # Auto-generate filename next to the source XML file
        input_dir=$(dirname "$input_file")
        base_name=$(basename "$input_file" .xml)
        final_output="$input_dir/${base_name}_report.html"
    fi
    
    # Make sure the file was created
    if [[ -f "$final_output" ]]; then
        echo ""
        echo -e "${GREEN}✅ Conversion completed successfully!${NC}"
        echo -e "${BLUE}📄 Report saved as: $final_output${NC}"
        echo -e "${BLUE}🌐 Full path: $(realpath "$final_output")${NC}"
        echo ""
        
        # Ask if user wants to open in browser, with 3 second timeout defaulting to N
        read -t 3 -p "Would you like to open the report in your browser? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open_in_browser "$final_output"
        else
            echo
        fi
    else
        echo -e "${RED}Error: Output file was not created${NC}"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"
