//
//  HomePageViewController.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/17/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import UIKit

class HomePageViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    @IBAction func AddTrip(_ sender: Any) {
         self.performSegue(withIdentifier: "add", sender: self)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
}




extension HomePageViewController: UITableViewDelegate,UITableViewDataSource{
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if UserDefault.currentUser?.trips != nil{
        return (UserDefault.currentUser?.trips!.count)!
       }
        else {return 0}
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let cell = tableView.dequeueReusableCell(withIdentifier: "cell", for: indexPath) as! TripsTableViewCell
        let trip = UserDefault.currentUser?.trips![indexPath.row]
        cell.startDate.text = trip?.startDate
        cell.tripName.text = trip?.name
        cell.destination.text = trip?.destination
        if trip?.status == true{
            cell.status.text = "completed"
        }
        else{
             cell.status.text = "In progress"
        }

        return cell
    }
    
    
}
