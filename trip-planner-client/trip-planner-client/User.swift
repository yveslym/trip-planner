//
//  User.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/12/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import Foundation

struct UserData: Codable {
    var firstName: String?
    var lastName: String?
    var email: String?
    var password:String?
    var credential: String?
    var trips: [Trip_Data]?
    var userID: String?
    
    enum userKey:String,CodingKey{
        case first_name
        case last_name
        case email
        case password
        case _id
    }
}

extension UserData {
    init(from decoder: Decoder) throws {
        let contenaire = try decoder.container(keyedBy: userKey.self)
        self.email = (try contenaire.decodeIfPresent(String.self, forKey: .email))!
        self.firstName = (try contenaire.decodeIfPresent(String.self, forKey: .first_name))!
        self.lastName = (try contenaire.decodeIfPresent(String.self, forKey: .last_name))!
        self.userID = (try contenaire.decodeIfPresent(String.self, forKey: ._id))
        self.password = ""
        var trip = [Trip_Data]()
        self.trips = nil
        
        Networking.operation(route: .fetchTrip, user: UserDefault.currentUser) { (data, resp) in
            do{
                guard let data = data else {return }
                trip = try JSONDecoder().decode([Trip_Data].self, from: data)
                UserDefault.currentUser?.trips = trip
            }
            catch{}
        }
       
    }
    
    func encode(to encoder: Encoder) throws {
        var contenaire = encoder.container(keyedBy: userKey.self)
        try contenaire.encode(firstName, forKey: .first_name)
        try contenaire.encode(lastName, forKey: .last_name)
        try contenaire.encode(email, forKey: .email)
        try contenaire.encode(password, forKey: .password)
    }
    
    init(email:String? = nil,password:String? = nil,firstName:String? = nil,lastName:String? = nil){
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
         self.credential = BasicAuth.generateBasicAuthHeader(user: self)
    }
}

struct Errors: Decodable{
    var error:String?
    
    init (error: String?){
        self.error = error
    }
    
    enum errorKey:String, CodingKey {
        case error
    }
    init(from decoder:Decoder)throws {
        let contenaire = try decoder.container(keyedBy: errorKey.self)
        let err = (try contenaire.decodeIfPresent(String.self, forKey: .error)) 
        self.init(error: err)
    }
}

struct Trip_Data: Codable{
    let name : String?
    let destination : String?
    let stopPoint : [String]?
    let status: Bool?
    let tripID:String?
    let startDate:String?
    let user: String?
    
    enum tripKey: String,CodingKey {
        case name
        case destination
        case stop_point
        case status
        case trip_id
        case start_date
        case user_id = "user_id"
        
    }
}

extension Trip_Data{
    
    init( name:String? = nil, destination:String? = nil, stop_point:[String]? = nil, status: Bool? = nil, startDate:String? = nil, tripID:String? = nil) {
        self.name = name
        self.destination = destination
        self.tripID = tripID
        self.stopPoint = stop_point
        self.status = status
        self.startDate = startDate
        self.user = UserDefault.currentUser?.userID
        
    }
    init(from decoder: Decoder)throws{
        
        let contenaire = try decoder.container(keyedBy: tripKey.self)
        let name = try contenaire.decodeIfPresent(String.self, forKey: .name)
        let user = try contenaire.decodeIfPresent(String.self, forKey: .user_id)
        let destination = try contenaire.decodeIfPresent(String.self, forKey: .destination)
        let start_date = try contenaire.decodeIfPresent(String.self, forKey: .start_date)
        let status = try contenaire.decodeIfPresent(Bool.self, forKey: .status)
         let tripID = try contenaire.decodeIfPresent(String.self, forKey: .trip_id)
        let endPoint = try contenaire.decodeIfPresent([String].self, forKey: .stop_point)
        
        
        self.init( name: name, destination: destination, stopPoint:endPoint, status: status, tripID: tripID, startDate: start_date, user:user)
        
    }
    
   func encode(to encoder: Encoder) throws {
    var contenaire = encoder.container(keyedBy: tripKey.self)
    try contenaire.encode(name, forKey: .name)
    try contenaire.encode(destination, forKey: .destination)
    try contenaire.encode(startDate, forKey: .start_date)
    try contenaire.encode(String(describing: status), forKey: .status)
    try contenaire.encode(user, forKey: .user_id)
    
    }

}












