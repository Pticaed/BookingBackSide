const { loadFixture } = require("@nomicfoundation/hardhat-toolbox/network-helpers");
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("BookingSystem", () => {
    async function deploy() {
        const [owner, guest, stranger] = await ethers.getSigners();
        const factory = await ethers.getContractFactory("BookingSystem");
        const c_booking = await factory.deploy();

        return { c_booking, owner, guest, stranger };
    }

    it("should allow to create a property", async () => {
        const { c_booking, owner } = await loadFixture(deploy);
        const price = ethers.parseEther("0.1");

        await c_booking.connect(owner).create_property(price);
        
        const properties = await c_booking.get_properties();
        expect(properties.length).to.equal(1);
        expect(properties[0].owner).to.equal(owner.address);
        expect(properties[0].price_per_night).to.equal(price);
    });

    it("should create a booking and lock funds in contract", async () => {
        const { c_booking, owner, guest } = await loadFixture(deploy);
        const price = ethers.parseEther("1.0");

        await c_booking.connect(owner).create_property(price);

        await expect(() =>
            c_booking.connect(guest).create_booking(0, 1715000000, 1715100000, { value: price })
        ).to.changeEtherBalance(c_booking, price);

        const bookings = await c_booking.get_bookings();
        expect(bookings[0].guest).to.equal(guest.address);
        expect(bookings[0].status).to.equal("confirmed");
    });

    it("should complete booking and transfer funds to property owner", async () => {
        const { c_booking, owner, guest } = await loadFixture(deploy);
        const price = ethers.parseEther("2.0");

        await c_booking.connect(owner).create_property(price);
        await c_booking.connect(guest).create_booking(0, 10, 20, { value: price });

        await expect(() =>
            c_booking.connect(guest).complete_booking(0)
        ).to.changeEtherBalance(owner, price);

        const bookings = await c_booking.get_bookings();
        expect(bookings[0].status).to.equal("Completed");
    });

    it("should allow guest to add a review", async () => {
        const { c_booking, owner, guest } = await loadFixture(deploy);
        
        await c_booking.connect(owner).create_property(ethers.parseEther("0.1"));
        await c_booking.connect(guest).create_booking(0, 1, 2, { value: ethers.parseEther("0.1") });

        const reviewCid = "QmTestReview";
        await c_booking.connect(guest).add_review(0, 5, reviewCid);

        const reviews = await c_booking.get_reviews();
        expect(reviews.length).to.equal(1);
        expect(reviews[0].rating).to.equal(5n);
        expect(reviews[0].ipfs_cid).to.equal(reviewCid);
    });

    it("should revert if stranger tries to complete booking", async () => {
        const { c_booking, owner, guest, stranger } = await loadFixture(deploy);
        
        await c_booking.connect(owner).create_property(ethers.parseEther("0.1"));
        await c_booking.connect(guest).create_booking(0, 1, 2, { value: ethers.parseEther("0.1") });

        await expect(
            c_booking.connect(stranger).complete_booking(0)
        ).to.be.revertedWith("Not auth");
    });
});