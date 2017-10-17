//
//  RegisterUIViewController.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/17/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import UIKit

class RegisterUIViewController: UIViewController {

    @IBOutlet weak var email: UITextField!
    
    @IBOutlet weak var password: UITextField!
    
    @IBOutlet weak var fname: UITextField!
    
    @IBOutlet weak var lname: UITextField!
    
      @IBOutlet weak var loginButton: UIButton!
    
    @IBOutlet weak var registerButton: UIButton!
    
    @IBOutlet weak var lastLabel: UILabel!
    @IBOutlet weak var firstlabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        fname.isHidden = true
        lname.isHidden = true
        lastLabel.isHidden = true
        firstlabel.isHidden = true
        // Do any additional setup after loading the view.
    }
    @IBAction func loginTapped(_ sender: Any) {
        
       
        
        if loginButton.titleLabel?.text == "Login"{
            
             let user = UserData(email: email.text, password: password.text)
            
            Networking.operation(route: .fetchUser, user: user, completion: { (data, response) in
                print(response)
            })
        }
        else {
            let user = UserData(email: email.text, password: password.text, firstName: fname.text, lastName: lname.text)
            Networking.operation(route: .createUser, user: user, completion: { (data, response) in
                print(response)
            })
        }
        
    }
    
    @IBAction func registerTapped(_ sender: Any) {
        if registerButton.titleLabel?.text == "Register?"{
            registerButton.titleLabel?.text = "Login"
            loginButton.titleLabel?.text = "Register"
            fname.isHidden = false
            lname.isHidden = false
            lastLabel.isHidden = false
            firstlabel.isHidden = false
            
           // self.loadView()
        }
        else if registerButton.titleLabel?.text == "Login"{
            registerButton.titleLabel?.text = "Register?"
            loginButton.titleLabel?.text = "Login"
           
            fname.isHidden = true
            lname.isHidden = true
            lastLabel.isHidden = true
            firstlabel.isHidden = true
            //self.loadView()
        }
        
    }
    
    
    

}
