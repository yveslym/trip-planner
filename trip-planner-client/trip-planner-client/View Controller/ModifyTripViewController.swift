//
//  ModifyTripViewController.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/21/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import UIKit

class ModifyTripViewController: UIViewController {

    @IBOutlet weak var destination: UILabel!
    
    @IBOutlet weak var startDate: UILabel!
    
    @IBOutlet weak var addTextField: UIStackView!
    
    @IBOutlet weak var stopPointTextField: UITextField!
    
    @IBOutlet weak var addStack: UIStackView!
     var myTrip: Trip_Data?
    
    let homePage = HomePageViewController()
    
    @IBOutlet weak var myTable: UITableView!
    @IBAction func displayTextField(_ sender: Any) {
        self.addTextField.isHidden = false
        
        self.reloadInputViews()
    }
    
    @IBAction func addButton(_ sender: Any) {
      // network put
        
    // hide
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.addTextField.isHidden = true
        self.addStack.isHidden = true
        self.myTable.delegate = self
        self.myTable.dataSource = self
        homePage.tripDelegate  = self
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}

extension ModifyTripViewController: UITableViewDelegate,UITableViewDataSource, TripProtocol{
   
    func passTrip(trip: Trip_Data?) {
        self.myTrip = trip
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        
        return (self.myTrip?.stopPoint?.count)!
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
         let cell = tableView.dequeueReusableCell(withIdentifier: "cell", for: indexPath) as! ListOfStopPointTableViewCell
        cell.stopPoint.text = myTrip?.stopPoint![indexPath.row]
    return cell
    }
    //==> get the data from tripProtocol
}










