//
//  Network.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/12/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import Foundation

class Network{
    
    // function to create a new user
    static func create_user(users:UserData!){
    
        let urlString = "http://127.0.0.1:5000/users"
        guard let url = URL(string: urlString) else {return}
        var request = URLRequest(url: url)
        
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "content-type")
        
        do{
            let jsonBody = try JSONEncoder().encode(users)
            request.httpBody = jsonBody
        }catch{}
        
        let session = URLSession.shared
        let task = session.dataTask(with: request){(data,response,error) in
            
            
            
            guard let data = data else {return}
            
            do{
                _ = try JSONSerialization.jsonObject(with: data, options: [])
            }catch{}
        
       
        
        if (error == nil) {
            // Success
            let statusCode = (response as! HTTPURLResponse).statusCode
            print("URL Session Task Succeeded: HTTP \(statusCode)")
            print(response?.description as Any)
        }
        else {
            // Failure
            let statusCode = (response as! HTTPURLResponse).statusCode
            print (statusCode)
            print("URL Session Task Failed: %@", error!.localizedDescription);
        }
        }
         task.resume()
    }
    
    static func create_trip(){
        
    }
    
    static func fetch_user(email: String, password: String){
      
        // get the auth header
      let authHeaderString =  BasicAuth.generateBasicAuthHeader(username: email, password: password)
        
        let urlString = "http://127.0.0.1:5000/users"
        guard let url = URL(string: urlString) else {return}
        var request = URLRequest(url: url)
        
        request.httpMethod = "GET"
        request.addValue("application/json", forHTTPHeaderField: "content-type")
        request.addValue(authHeaderString, forHTTPHeaderField: "Authorization")
        
        let session = URLSession.shared
        let task = session.dataTask(with: request){(data,response,error) in
            
            guard let data = data else {return}
            
            do{
                let user = try JSONDecoder().decode(UserData.self, from: data)
                print (user)
            }
            catch{}
        }
        task.resume()
    }
    
    static func deleteUser(email:String, password: String){
        
        let authHeaderString = BasicAuth.generateBasicAuthHeader(username: email, password: password)
        
        let urlString = "http://127.0.0.1:5000/users"
        guard let url = URL(string: urlString) else {return}
        var request = URLRequest(url: url)
        
    }
    
}


struct BasicAuth {
    static func generateBasicAuthHeader(username: String, password: String) -> String {
        let loginString = String(format: "%@:%@", username, password)
        let loginData: Data = loginString.data(using: String.Encoding.utf8)!
        let base64LoginString = loginData.base64EncodedString(options: .init(rawValue: 0))
        let authHeaderString = "Basic \(base64LoginString)"
        
        return authHeaderString
    }
}
