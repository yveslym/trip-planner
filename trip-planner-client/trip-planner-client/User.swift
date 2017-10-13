//
//  User.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/12/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import Foundation

class User{
    
    let first_name: String
    let last_name: String
    let email: String
    var trips : [Trip]
    
    init (fname:String,lname:String,email:String,trips:[Trip]){
        self.first_name = fname
        self.last_name = lname
        self.email = email
        self.trips = trips
    }
}

class Trip{
    let name : String
    let destination : String
    let stop_point : [String]
    let status: Bool
    
    init(name:String,destination:String,status:Bool,s_point:[String]){
        self.destination = destination
        self.name = name
        self.status = status
        self.stop_point = s_point
    }
}


