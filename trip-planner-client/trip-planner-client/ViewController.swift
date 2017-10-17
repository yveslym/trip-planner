//
//  ViewController.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/12/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    var user = UserData(email: "yves2300@yahoo.fr", password: "123456", firstName: "yves", lastName: "songolo")
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func addUser(_ sender: Any) {
        
        Networking.operation(route: .createUser, user: user) { (data, response) in
            print (response)
        }
    }
    @IBAction func getUser(_ sender: Any) {
       
        Networking.operation(route: .fetchUser, user: user) { (data, response) in
            print(response)
        }
    }
    @IBAction func deleteUser(_ sender: Any) {
        Networking.operation(route: .deleteUser, user: user) { (data, response) in
            print(response)
        }
    }
    
    @IBAction func getTrip(_ sender: Any) {
      
    }
    @IBAction func post(_ sender: Any) {
        
    }
    
    @IBAction func deleteTrips(_ sender: Any) {
     //Networking.operation(route: .deleteTrip, user: user, trip: trip, completion: <#T##(Data?, Int) -> Void#>)
    }
    @IBOutlet weak var deleteTrip: UIButton!
    
}

