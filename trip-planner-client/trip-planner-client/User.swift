//
//  User.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/12/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import Foundation

struct UserData: Codable {
    var firstName: String
    var lastName: String
    var email: String
    var password:String
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
    
    init(email:String,password:String,firstName:String,lastName:String){
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
    let name : String
    let destination : String
    let stopPoint : [String]
    let status: Bool
    
    enum tripKey: String,CodingKey {
        case name
        case destination
        case stop_point
        case status
    }
}












