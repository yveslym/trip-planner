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
    
    static func create_trip(user:UserData,trip:Trip_Data){
        
        let urlString = "http://127.0.0.1:5000/users"
        guard let url = URL(string: urlString) else {return}
        var request = URLRequest(url: url)
    
        
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "content-type")
        
        do{
            
            let jsonBody = try JSONEncoder().encode(trip)
            request.httpBody = jsonBody
        }catch{}
        
        
        let session = URLSession.shared
        let task = session.dataTask(with: request){data,response,Error in
          
         
            
            do{
                
            }
            catch{}
        }
        task.resume()
    }
    
    static func get_trip(user:UserData){
        
    }
    
    static func delete_trip(user:UserData){
        
    }
    
    // function to get user from the database by the auth token
    static func fetch_user(user:UserData){
      
        // get the auth header
        
        let urlString = "http://127.0.0.1:5000/users"
        guard let url = URL(string: urlString) else {return}
        var request = URLRequest(url: url)
        
        request.httpMethod = "GET"
        request.addValue("application/json", forHTTPHeaderField: "content-type")
        request.addValue(user.credential!, forHTTPHeaderField: "Authorization")
        
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
    
    ///function to delete user by with the auth token
    static func deleteUser(user:UserData){
        
      
        
        let urlString = "http://127.0.0.1:5000/users"
        guard let url = URL(string: urlString) else {return}
        var request = URLRequest(url: url)
        
        request.httpMethod = "DELETE"
        request.addValue("application/json", forHTTPHeaderField: "content-type")
        request.addValue(user.credential!, forHTTPHeaderField: "Authorization")
        
        let session = URLSession.shared
        let task = session.dataTask(with: request){(data,response,error)in
            do{
                if (error == nil) {
                    // Success
                    let statusCode = (response as! HTTPURLResponse).statusCode
                    _ = (response as? HTTPURLResponse)?.textEncodingName
                    print("URL Session Task Succeeded: HTTP \(statusCode)")
                    
                    if statusCode == 400 || statusCode == 401{
                    //let responseData = String(data: data!, encoding: String.Encoding.utf8)!
                        let errorMessage = try JSONDecoder().decode(Errors.self, from: data!)
                    print (errorMessage.error)
                    }
                    
                }
                else {
                    // Failure
                    let statusCode = (response as! HTTPURLResponse).statusCode
                    print (statusCode)
                    print("URL Session Task Failed: %@", error!.localizedDescription)
                }
            }
            catch {}
        }
        task.resume()
    }
}


struct BasicAuth {
    static func generateBasicAuthHeader(user:UserData) -> String {
        let loginString = String(format: "%@:%@", user.email, user.password)
        let loginData: Data = loginString.data(using: String.Encoding.utf8)!
        let base64LoginString = loginData.base64EncodedString(options: .init(rawValue: 0))
        let authHeaderString = "Basic \(base64LoginString)"
        
        return authHeaderString
    }
}



