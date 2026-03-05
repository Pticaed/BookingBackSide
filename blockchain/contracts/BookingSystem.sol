// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BookingSystem {
    event NewBooking(uint indexed id, uint indexed property_id, address guest, uint amount);
    event BookingStatusChanged(uint indexed id, string status);

    struct Property {
        uint id;
        address owner;
        uint price_per_night;
        bool is_active;
        bool exists;
    }

    struct Booking {
        uint id;
        uint property_id;
        address guest;
        uint check_in;
        uint check_out;
        uint total_amount;
        string status;
        bool exists;
    }

    struct Review {
        uint id;
        uint booking_id;
        uint rating;
        string ipfs_cid;
        bool exists;
    }

    Property[] public properties;
    Booking[] public bookings;
    Review[] public reviews;

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function create_property(uint _price_per_night) external {
        properties.push(Property(properties.length, msg.sender, _price_per_night, true, true));
    }

    function create_booking(uint _property_id, uint _check_in, uint _check_out) external payable {
        require(properties[_property_id].exists, "No property");
        require(properties[_property_id].is_active, "Not active");
        require(msg.value > 0, "Zero payment");

        bookings.push(Booking(
            bookings.length,
            _property_id,
            msg.sender,
            _check_in,
            _check_out,
            msg.value,
            "confirmed",
            true
        ));

        emit NewBooking(bookings.length - 1, _property_id, msg.sender, msg.value);
    }

    function complete_booking(uint _id) external {
        require(bookings[_id].exists, "No booking");
        require(msg.sender == bookings[_id].guest || msg.sender == owner, "Not auth");

        bookings[_id].status = "Completed";
        
        uint prop_id = bookings[_id].property_id;
        address payable prop_owner = payable(properties[prop_id].owner);
        
        prop_owner.transfer(bookings[_id].total_amount);
        emit BookingStatusChanged(_id, "Completed");
    }

    function cancel_booking(uint _id) external {
        require(bookings[_id].exists, "No booking");
        require(msg.sender == bookings[_id].guest || msg.sender == owner, "Not auth");

        bookings[_id].status = "Cancelled";
        
        address payable guest = payable(bookings[_id].guest);
        guest.transfer(bookings[_id].total_amount);
        
        emit BookingStatusChanged(_id, "Cancelled");
    }

    function add_review(uint _booking_id, uint _rating, string memory _cid) external {
        require(bookings[_booking_id].exists, "No booking");
        require(bookings[_booking_id].guest == msg.sender, "Not guest");

        reviews.push(Review(reviews.length, _booking_id, _rating, _cid, true));
    }

    function get_properties() external view returns (Property[] memory) {
        return properties;
    }

    function get_bookings() external view returns (Booking[] memory) {
        return bookings;
    }

    function get_reviews() external view returns (Review[] memory) {
        return reviews;
    }
}