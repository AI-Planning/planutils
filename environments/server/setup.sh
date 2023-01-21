
# Check if argument is build or run
if [ "$1" = "build" ]; then
    # Build
    echo "Building..."
    docker build -t planutils-server .
    echo "Done."
    exit 0
elif [ "$1" = "run" ]; then
    # Run
    echo "Running..."
    docker run --privileged -p 5555:5555 -d planutils-server
    echo "Done."
    exit 0
else
    # Print usage
    echo "Usage: setup.sh build|run"
    exit 1
fi
