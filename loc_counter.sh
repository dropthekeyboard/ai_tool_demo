#!/bin/bash
# filepath: /home/fritzprix/corp_works/ai_tool_demo/loc_counter.sh
# Script to count lines and words in text files

usage() {
    echo "Usage: $0 [options] [file|directory...]"
    echo
    echo "Options:"
    echo "  -a, --all         Count all lines (default)"
    echo "  -n, --non-empty   Count non-empty lines only"
    echo "  -c, --code        Count non-comment lines (basic comment detection)"
    echo "  -w, --words       Count words instead of lines"
    echo "  -r, --recursive   Process directories recursively"
    echo "  -t, --total       Show total count only"
    echo "  -h, --help        Display this help message"
    echo
    echo "If no file or directory is specified, processes all text files in current directory."
    exit 1
}

count_all_lines() {
    wc -l "$1" | awk '{print $1}'
}

count_non_empty_lines() {
    grep -c -v "^[ \t]*$" "$1"
}

count_code_lines() {
    grep -v "^[ \t]*#\|^[ \t]*\/\/\|^[ \t]*\/\*\|^[ \t]*\*\|^[ \t]*\*\/\|^[ \t]*$" "$1" | wc -l
}

count_all_words() {
    wc -w "$1" | awk '{print $1}'
}

count_non_empty_words() {
    grep -v "^[ \t]*$" "$1" | wc -w
}

count_code_words() {
    grep -v "^[ \t]*#\|^[ \t]*\/\/\|^[ \t]*\/\*\|^[ \t]*\*\|^[ \t]*\*\/\|^[ \t]*$" "$1" | wc -w
}

# Default settings
MODE="all"
COUNT_TYPE="lines"
RECURSIVE=false
TOTAL_ONLY=false
TOTAL=0
FILES_COUNTED=0

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        -a|--all)
            MODE="all"
            shift
            ;;
        -n|--non-empty)
            MODE="non_empty"
            shift
            ;;
        -c|--code)
            MODE="code"
            shift
            ;;
        -w|--words)
            COUNT_TYPE="words"
            shift
            ;;
        -r|--recursive)
            RECURSIVE=true
            shift
            ;;
        -t|--total)
            TOTAL_ONLY=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "Unknown option: $1"
            usage
            ;;
        *)
            break
            ;;
    esac
done

# If no files/dirs specified, use current directory
if [[ $# -eq 0 ]]; then
    set -- "."
fi

# Process each file/directory
for TARGET in "$@"; do
    if [[ -f "$TARGET" ]]; then
        # Process single file
        if [[ "$COUNT_TYPE" == "lines" ]]; then
            case "$MODE" in
                all)
                    COUNT=$(count_all_lines "$TARGET")
                    ;;
                non_empty)
                    COUNT=$(count_non_empty_lines "$TARGET")
                    ;;
                code)
                    COUNT=$(count_code_lines "$TARGET")
                    ;;
            esac
        else  # Count words
            case "$MODE" in
                all)
                    COUNT=$(count_all_words "$TARGET")
                    ;;
                non_empty)
                    COUNT=$(count_non_empty_words "$TARGET")
                    ;;
                code)
                    COUNT=$(count_code_words "$TARGET")
                    ;;
            esac
        fi
        
        if [[ "$TOTAL_ONLY" == false ]]; then
            echo "$TARGET: $COUNT ${COUNT_TYPE}"
        fi
        
        TOTAL=$((TOTAL + COUNT))
        FILES_COUNTED=$((FILES_COUNTED + 1))
        
    elif [[ -d "$TARGET" ]]; then
        # Process directory
        if [[ "$RECURSIVE" == true ]]; then
            FIND_CMD="find \"$TARGET\" -type f -not -path \"*/\.*\" | sort"
        else
            FIND_CMD="find \"$TARGET\" -maxdepth 1 -type f -not -path \"*/\.*\" | sort"
        fi
        
        while IFS= read -r FILE; do
            if [[ -f "$FILE" && -r "$FILE" ]]; then
                if [[ "$COUNT_TYPE" == "lines" ]]; then
                    case "$MODE" in
                        all)
                            COUNT=$(count_all_lines "$FILE")
                            ;;
                        non_empty)
                            COUNT=$(count_non_empty_lines "$FILE")
                            ;;
                        code)
                            COUNT=$(count_code_lines "$FILE")
                            ;;
                    esac
                else  # Count words
                    case "$MODE" in
                        all)
                            COUNT=$(count_all_words "$FILE")
                            ;;
                        non_empty)
                            COUNT=$(count_non_empty_words "$FILE")
                            ;;
                        code)
                            COUNT=$(count_code_words "$FILE")
                            ;;
                    esac
                fi
                
                if [[ "$TOTAL_ONLY" == false ]]; then
                    echo "$FILE: $COUNT ${COUNT_TYPE}"
                fi
                
                TOTAL=$((TOTAL + COUNT))
                FILES_COUNTED=$((FILES_COUNTED + 1))
            fi
        done < <(eval $FIND_CMD)
    else
        echo "Warning: $TARGET is not a file or directory, skipping."
    fi
done

# Print total
if [[ $FILES_COUNTED -gt 1 || "$TOTAL_ONLY" == true ]]; then
    echo "Total: $TOTAL ${COUNT_TYPE} in $FILES_COUNTED files"
fi

exit 0