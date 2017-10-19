//
//  AddTripViewController.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/18/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import UIKit

class AddTripViewController: UIViewController {
   
    @IBOutlet weak var name: UITextField!
    
    @IBOutlet weak var destiination: UITextField!
    
    @IBOutlet weak var start_date: UITextField!
    
    @IBAction func addTrip(_ sender: Any) {
        
        let trip = Trip_Data(name: name.text, destination: destiination.text, status: false, startDate: start_date.text)
                    UserDefault.currentUser?.trips?.append(trip)
        
//        Networking.operation(route:.createTrip, user: UserDefault.currentUser, trip: trip) {(data, resp) in
//            print(resp)
        Networking.operation(route: .createTrip, user: UserDefault.currentUser,trip: trip ,completion: { (data, response) in
            print(response)
            
            guard let data = data else{return}
            do{
            let newTrip = try JSONDecoder().decode(Trip_Data.self, from: data)
            
            UserDefault.currentUser?.trips?.append(newTrip)
        
            }
            catch {}
        })
    }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
