const { ethers } = require("hardhat");

(async () => {
    console.log("starting deployment...");
    const factory = await ethers.getContractFactory("BookingSystem");
    const contract = await factory.deploy();
    await contract.waitForDeployment();
    console.log("BookingSystem deployed at:", await contract.getAddress());
    
})().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});