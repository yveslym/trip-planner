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
    
    enum userKey:String,CodingKey{
        case first_name
        case last_name
        case email
        case password
    }
}

extension UserData {
    init(from decoder: Decoder) throws {
        let contenaire = try decoder.container(keyedBy: userKey.self)
        email = (try contenaire.decodeIfPresent(String.self, forKey: .email))!
        firstName = (try contenaire.decodeIfPresent(String.self, forKey: .first_name))!
        lastName = (try contenaire.decodeIfPresent(String.self, forKey: .last_name))!
        password = ""
        
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
    var error:String
    
    enum errorKey:String, CodingKey {
        case error
    }
    init(from decoder:Decoder)throws {
        let contenaire = try decoder.container(keyedBy: errorKey.self)
         error = (try contenaire.decodeIfPresent(String.self, forKey: .error))!
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
        case user
    }
}

extension Trip_Data{
    
    init(CreateBy user: UserData? = nil, name:String? = nil, destination:String? = nil, stop_point:[String]? = nil, status: Bool? = nil, startDate:String? = nil, tripID:String? = nil) {
        self.name = name
        self.destination = destination
        self.tripID = tripID
        self.stopPoint = stop_point
        self.status = status
        self.startDate = startDate
        self.user = user?.email
    }
    init(from decoder: Decoder)throws{
        
        let contenaire = try decoder.container(keyedBy: tripKey.self)
        let name = try contenaire.decodeIfPresent(String.self, forKey: .name)
        let user = try contenaire.decodeIfPresent(String.self, forKey: .user)
        let destination = try contenaire.decodeIfPresent(String.self, forKey: .destination)
        let start_date = try contenaire.decodeIfPresent(String.self, forKey: .start_date)
        let status = try contenaire.decodeIfPresent(Bool.self, forKey: .status)
         let tripID = try contenaire.decodeIfPresent(String.self, forKey: .trip_id)
        // implement
        
        self.init( name: name, destination: destination, status: status, startDate: start_date, tripID: tripID)
        
    }

}












