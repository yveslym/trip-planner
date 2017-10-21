//
//  HomePageViewController.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/17/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import UIKit

class HomePageViewController: UIViewController {

    
    weak var tripDelegate: TripProtocol?
    @IBOutlet weak var mytable: UITableView!
    override func viewDidLoad() {
        super.viewDidLoad()
        
        mytable.delegate = self
        mytable.dataSource = self
        
        // Do any additional setup after loading the view.
    }
    @IBAction func AddTrip(_ sender: Any) {
         self.performSegue(withIdentifier: "add", sender: self)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewWillAppear(_ animated: Bool) {
//        Networking.operation(route: .fetchTrip, user: UserDefault.currentUser) { (data, resp) in
//
//            do{
//                guard let data = data else {return}
//                let list = try JSONDecoder().decode(ListOfTrip?.self, from: data)
//                guard let trips = list else{return}
//
//                UserDefault.currentUser?.myTrips = trips
//                self.mytable.reloadData()
//            }
//
//            catch{}
//        }
        Networking.operation(route: .fetchTrip, user: UserDefault.currentUser) { (data, resp) in
            
            do{
                guard let data = data else {return}
                let list = try JSONDecoder().decode([Trip_Data]?.self, from: data)
                guard let trips = list else{return}
                
                print(trips)
                
                DispatchQueue.main.async {
                    UserDefault.currentUser?.myTrips = trips
                    self.mytable.reloadData()
                }
                
            }
                
            catch{}
        }
        
    }
}




extension HomePageViewController: UITableViewDelegate,UITableViewDataSource{
    
    
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        
        if UserDefault.currentUser?.myTrips != nil{
            return (UserDefault.currentUser?.myTrips?.count)!
       }
        else {return 0}
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let cell = tableView.dequeueReusableCell(withIdentifier: "cell", for: indexPath) as! TripsTableViewCell
        let trip = UserDefault.currentUser?.myTrips![indexPath.row]
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
     func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        
        tripDelegate?.passTrip(trip: UserDefault.currentUser?.myTrips![indexPath.row])
    }
    
}





























