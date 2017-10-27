//
//  Notification center.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/17/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import Foundation

class UserSender{
    
}
class UserDefault{
    static var currentUser: UserData?
//==> static func to archive basic auth
    static func archiveCredential(user: UserData){
        let credentail = BasicAuth.generateBasicAuthHeader(user: user)
        let data = NSKeyedArchiver.archivedData(withRootObject: credentail)
        UserDefaults.standard.set(data, forKey: "saved_credential")
        
        
    }
//==> static func to unarchive basic auth and return a string
    static func unarchiveCredential(){
        if let data = UserDefaults.standard.data(forKey: "saved_credential"){
            let credential = NSKeyedUnarchiver.unarchiveObject(with: data)
            UserDefault.currentUser?.credential = credential as? String
        }
    }
//==> function to retrieve user info if user ever login before
    static func Relogin(){
       
        Networking.operation(route: .fetchUser, user: UserDefault.currentUser) { (data, response) in
            
            guard let data = data else {return}
            do{
                UserDefault.currentUser = try! JSONDecoder().decode(UserData.self, from: data)
            }
        }
    }
}
