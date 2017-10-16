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
        
        
        
        Network.create_user(users: self.user)
    }
    @IBAction func getUser(_ sender: Any) {
        Network.fetch_user(user: self.user)
    }
    @IBAction func deleteUser(_ sender: Any) {
        Network.deleteUser(user: self.user)
    }
    
    @IBAction func getTrip(_ sender: Any) {
        Network.create_trip()
    }
    @IBAction func post(_ sender: Any) {
        
    }
    
    @IBAction func deleteTrips(_ sender: Any) {
        
    }
    @IBOutlet weak var deleteTrip: UIButton!
    
}

