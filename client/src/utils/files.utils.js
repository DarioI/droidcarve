export function ext(filename) {
    return filename.toLowerCase().trim().split('.').pop();
}