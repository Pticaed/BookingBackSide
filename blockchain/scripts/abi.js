const fs = require('fs');
const path = require('path');

(async () => {
    const artifactPath = path.resolve(__dirname, "../artifacts/contracts/BookingSystem.sol/BookingSystem.json");
    const outputPath = path.resolve(__dirname, "../../blockchain_abi/BookingSystem.json");
    const artifact = JSON.parse(fs.readFileSync(artifactPath, 'utf8'));
    const dir = path.dirname(outputPath);

    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(outputPath, JSON.stringify(artifact.abi, null, 2));
    
    console.log(`abi exported to: ${outputPath}`);

})().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});