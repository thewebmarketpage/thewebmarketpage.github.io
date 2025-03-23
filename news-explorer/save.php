<?php
$dataFile = 'data.json';

// Function to generate unique ID
function generateId() {
    // Use current timestamp + random hex
    return uniqid();
}

// Get POST body
$input = file_get_contents('php://input');
$newEntry = json_decode($input, true);

if ($newEntry) {
    // Read existing data
    $existing = [];
    if (file_exists($dataFile)) {
        $json = file_get_contents($dataFile);
        $existing = json_decode($json, true);
    }

    // Add generated ID
    $newEntry['id'] = generateId();

    // Append new entry
    $existing[] = $newEntry;

    // Save back to data.json
    file_put_contents($dataFile, json_encode($existing, JSON_PRETTY_PRINT));

    echo "Data saved! ID: " . $newEntry['id'];
} else {
    echo "Invalid data!";
}
?>

