//
//  Archiving.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/25/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import Foundation

extension UserData{
    func archiveUser(user: UserData){
        // turn userinto a data format(keychain)
        let data = NSKeyedArchiver.archivedData(withRootObject: user)
        
        // save into the crypted user
        UserDefaults.standard.set(data, forKey: "user")
    }
    func unarchiveUser(){
         NSKeyedUnarchiver.unarchiveObject(withFile: "user")
    }

}


