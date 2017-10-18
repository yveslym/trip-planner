//
//  TripsTableViewCell.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/17/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import UIKit

class TripsTableViewCell: UITableViewCell {

    @IBOutlet weak var tripName: UILabel!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }
    @IBOutlet weak var destination: UILabel!
    @IBOutlet weak var startDate: UILabel!
    @IBOutlet weak var status: UILabel!
    
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
