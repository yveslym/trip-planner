//
//  ListOfStopPointTableViewCell.swift
//  trip-planner-client
//
//  Created by Yveslym on 10/21/17.
//  Copyright © 2017 Yveslym. All rights reserved.
//

import UIKit

class ListOfStopPointTableViewCell: UITableViewCell {
    @IBOutlet weak var stopPoint: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
