//
//  Networking.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/16/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import Foundation

enum Route{
    case fetchUser
    case createUser
    case deleteUser
    case fetchTrip
    case createTrip
    case deleteTrip
    
    //==> operation 1. function to pass the the path base on the case requieremnent
    
    func path()->String{
        switch self {
        case .createUser: fallthrough
        case .fetchUser: fallthrough
        case .deleteUser:
            return "/users"
        case .fetchTrip: fallthrough
        case .createTrip: fallthrough
        case .deleteTrip:
            return "/trips"
        }
    }
    //==> operation 2. function to get the url param base on case requierement
    
    func URLparameters(trip:Trip_Data? = nil, user:UserData? = nil)->[String:String]?{
        switch self {
        case .createUser:
            let param = ["first_name":user?.firstName, "last_name":user?.lastName]
            return param as? [String : String]
       
        case .deleteTrip:
            let param = ["trip_id":trip?.tripID]
            return param as? [String : String]
    
        case .createTrip:
            let param = ["name":trip?.name,
                         "destination":trip?.destination,
                         "stop_point":trip?.stopPoint![0],
                         "start_date":trip?.startDate]
            return param as? [String : String]
            
        case .fetchTrip: fallthrough
        case .fetchUser: fallthrough
        case .deleteUser:
            return nil
        }
    }
    
    //==> operation 3. function to pass Headers parameters base on case requierement
    
    func headers(user:UserData? = nil) -> [String:String] {
        switch self {
        case .createTrip: fallthrough
        case .createUser:
            return ["content-type":"application/json"]
        case .deleteTrip: fallthrough
        case .deleteUser: fallthrough
        case .fetchTrip: fallthrough
        case .fetchUser:
            return ["content-type":"application/json",
                    "Authorization":(user?.credential)!]
        }
    }
    
    //==>> operation 4. function to pass http Method base on case requierement
    func httpMethod()-> String{
        
        switch self {
        case .createTrip: fallthrough
        case .createUser:
            return "POST"
        case .deleteTrip: fallthrough
        case .deleteUser:
            return "DELETE"
        case .fetchUser: fallthrough
        case .fetchTrip:
            return "GET"
        }
    }
    //==>> operation 5. function to pass jsonBody
    func jsonBody(user:UserData? = nil, trip: Trip_Data? = nil)->Data?{
     
        switch self {
        case .createUser:
            var jsonBody = Data()
            do{
                 jsonBody = try JSONEncoder().encode(user)
            }catch{}
        return jsonBody
         
          //  encode user and return the data
        case .createTrip: fallthrough
        case .deleteTrip:
            var jsonBody = Data()
            do{
                jsonBody = try JSONEncoder().encode(trip)
            }catch{}
            return jsonBody
            
            
        case .deleteUser: fallthrough
        case .fetchUser: fallthrough
        case .fetchTrip:
            return nil
        }
    }
}

class Networking{
    
    //==> single method to fetch, create and delete both user and trip
    static func operation(route:Route, user:UserData? = nil,trip: Trip_Data? = nil, completion: @escaping(Data?, Int)->Void){
        
        // 1. set the url path
        let baseURL = "http://127.0.0.1:8080"
        var url = URL(string: "\(baseURL)\(route.path())")
        
        // 2. check the urlparam condition
        
        if user != nil && route.URLparameters(user:user) != nil{
            url = url?.appendingQueryParameters(route.URLparameters(user: user)!)
        }
        else if trip != nil && route.URLparameters(trip:trip) != nil {
            url = url?.appendingQueryParameters(route.URLparameters(trip: trip)!)
        }
        
        var request = URLRequest(url: url!)
        
        // 3. check headers condition
        if user != nil{
        request.allHTTPHeaderFields = route.headers(user: user)
        }
        else{
            request.allHTTPHeaderFields = route.headers()
        }
        //4. check the http method
        request.httpMethod = route.httpMethod()
        
        // 5. check for the json body
        
        if user != nil{
            request.httpBody = route.jsonBody(user: user)
        }
        else if trip != nil {
            request.httpBody = route.jsonBody( trip: trip)
        }
        
        let session = URLSession.shared
        let task = session.dataTask(with: request){data,response,error in
            if error != nil{
                print("error")
                print("here")
            }
            do{
            guard let data = data else {return}
                let statusCode = (response as! HTTPURLResponse).statusCode
                 return completion(data,statusCode)
            }
            catch{}
        }
        task.resume()
    }
}
struct BasicAuth {
    static func generateBasicAuthHeader(user:UserData) -> String {
        let loginString = String(format: "%@:%@", user.email!, user.password!)
        let loginData: Data = loginString.data(using: String.Encoding.utf8)!
        let base64LoginString = loginData.base64EncodedString(options: .init(rawValue: 0))
        let authHeaderString = "Basic \(base64LoginString)"
        
        return authHeaderString
}
}


























