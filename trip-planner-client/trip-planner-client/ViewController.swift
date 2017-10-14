//
//  ViewController.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/12/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func addUser(_ sender: Any) {
        
        let user = UserData(firstName:"yvesl", lastName:  "songolo", email:  "yves2300@mail.com", password: "123456")
        
        Network.create_user(users: user)
    }
    @IBAction func getUser(_ sender: Any) {
        Network.fetch_user(email: "yves2300@mail.com", password: "123456")
    }
    @IBAction func deleteUser(_ sender: Any) {
        Network.deleteUser(email: "yves2300@mail.com", password: "123456")
    }
    
}

