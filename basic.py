#Copyright [2019] [Supriyo Chowdhury]

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.











import json
import datetime
import time
import os
import dateutil.parser
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# --- Helpers that build all of the responses ---


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def build_response_card(title, subtitle, options):
    """
    Build a responseCard with a title, subtitle, and an optional set of options which should be displayed as buttons.
    """
    buttons = None
    if options is not None:
        buttons = []
        for i in range(min(5, len(options))):
            buttons.append(options[i])

    return {
        'contentType': 'application/vnd.amazonaws.card.generic',
        'version': 1,
        'genericAttachments': [{
            'title': title,
            'subTitle': subtitle,
            'buttons': buttons
        }]
    }

# --- Helper Functions ---



def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None





def isvalid_color_type(color_type):
    color_types = ['black and white', 'color']
    return color_type.lower() in color_types
    
def isvalid_color_typea(color_typea):
    color_typesa = ['black and white', 'color']
    return color_typea.lower() in color_typesa    


def isvalid_conc_type(conc_type):
    conc_types = ['Ethernet Wired', 'WiFi Wireless']
    return conc_type in conc_types

def isvalid_conc_typea(conc_typea):
    conc_typesa = ['Ethernet Wired', 'WiFi Wireless']
    return conc_typea in conc_typesa    


def isvalid_paper_size(paper_size):
    paper_sizes = ['Letter Legal', 'Letter Legal 11x17']
    return paper_size.lower() in paper_sizes
    
def isvalid_paper_sizea(paper_sizea):
    paper_sizesa = ['Letter Legal', 'Letter Legal 11x17']
    return paper_sizea.lower() in paper_sizesa    

def isvalid_print_type(print_types):
    print_type = ['Print Only', 'Print Copy Scan','Print Copy Scan Fax']
    return print_type.lower() in print_types
    
def isvalid_print_typea(print_typesa):
    print_typea = ['Print Only', 'Print Copy Scan','Print Copy Scan Fax']
    return print_typea.lower() in print_typesa    




def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def validate_machines(slots):
    color_type = try_ex(lambda: slots['slotFour'])
    conc_type = try_ex(lambda: slots['slotThree'])
    paper_size = try_ex(lambda: slots['slotOne'])
    print_type = try_ex(lambda: slots['slotTwo'])

    if color_type and not isvalid_color_type(color_type):
        return build_validation_result(
            False,
            'slotFour',
            'Enter a valid color choice'
        )
        
    if conc_type and not isvalid_conc_type(conc_type):
        return build_validation_result(
            False,
            'slotThree',
            'CONNECTION TYPES USB is the standard for connecting to a single computer. An Ethernet port can connect the printer to your network, so it is easy for multiple users to print. It is a very reliable connection. A WiFi enabled printer can connect wirelessly to your wireless network. Some printers have a wireless direct capability where computers can connect directly to the printer without going through a router or existing wireless network. If in doubt, choose WiFi. There are apps available, that let you print from a mobile device. There are other ways of connecting, including cloud printing, that are outside the scope of this bot.'
        )    

    return {'isValid': True}


def validate_machinesa(slots):
    color_typea = try_ex(lambda: slots['slotSup'])
    conc_typea = try_ex(lambda: slots['slotBap'])
    paper_sizea = try_ex(lambda: slots['slotBan'])
    print_typea = try_ex(lambda: slots['slotRan'])

    if color_typea and not isvalid_color_typea(color_typea):
        return build_validation_result(
            False,
            'slotSup',
            'Enter a valid color choice'
        )
        
    if conc_typea and not isvalid_conc_typea(conc_typea):
        return build_validation_result(
            False,
            'slotBap',
            'CONNECTION TYPES USB is the standard for connecting to a single computer. An Ethernet port can connect the printer to your network, so it is easy for multiple users to print. It is a very reliable connection. A WiFi enabled printer can connect wirelessly to your wireless network. Some printers have a wireless direct capability where computers can connect directly to the printer without going through a router or existing wireless network. If in doubt, choose WiFi. There are apps available, that let you print from a mobile device. There are other ways of connecting, including cloud printing, that are outside the scope of this bot.'
        )    

    return {'isValid': True}



""" --- Functions that control the bot's behavior --- """


def get_recommendation(intent_request):
    """
    

    Beyond fulfillment, the implementation for this intent demonstrates the following:
    1) Use of elicitSlot in slot validation and re-prompting
    2) Use of sessionAttributes to pass information that can be used to guide conversation
    """

    color_type = try_ex(lambda: intent_request['currentIntent']['slots']['slotFour'])
    conc_type = try_ex(lambda: intent_request['currentIntent']['slots']['slotThree'])
    

    paper_size = try_ex(lambda: intent_request['currentIntent']['slots']['slotOne'])
    print_type = try_ex(lambda: intent_request['currentIntent']['slots']['slotTwo'])
    
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    # Load confirmation history and track the current reservation.
    reservation = json.dumps({
        'color_type': color_type,
        'conc_type': color_type,
        'PaperSize': paper_size,
        'Print-type': print_type,
    
    })

    session_attributes['currentReservation'] = reservation

    
    validation_result = validate_machines(intent_request['currentIntent']['slots'])
    if not validation_result['isValid']:
        slots = intent_request['currentIntent']['slots']
        slots[validation_result['violatedSlot']] = None

        return elicit_slot(
            session_attributes,
            intent_request['currentIntent']['name'],
            slots,
            validation_result['violatedSlot'],
            validation_result['message']
        )

    #1111    
    if color_type=="black and white" and conc_type=="Ethernet Wired" and paper_size=="Letter Legal" and print_type=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother HL-L2350DW   $99 . '
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother HL-L2350DW',
            'subTitle': 'Brother HL-L2350DW',
            'attachmentLinkUrl': 'https://amzn.to/2QfRak4',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/71ryWtmAATL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}

    #1112
    if color_type=="black and white" and conc_type=="Ethernet Wired" and paper_size=="Letter Legal" and print_type=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother Brother MFC-L2750dw  . I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}

    #1113
    if color_type=="black and white" and conc_type=="Ethernet Wired" and paper_size=="Letter Legal" and print_type=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.Brother MFC-L2750dw'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}
    
    #1211
    if color_type=="black and white" and conc_type=="WiFi Wireless" and paper_size=="Letter Legal" and print_type=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.  Brother HL-L2350DW   $99'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother HL-L2350DW',
            'subTitle': 'Brother HL-L2350DW',
            'attachmentLinkUrl': 'https://amzn.to/2QfRak4',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/71ryWtmAATL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}    
    #1121
    if color_type=="black and white" and conc_type=="Ethernet Wired" and paper_size=="Letter Legal 11x17" and print_type=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh SP 6430DN',
            'subTitle': 'Ricoh SP 6430DN. The sturdy, low cost per page option.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01132XDD4/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01132XDD4&linkId=1a6d750fc8b8a2ae6daebb4b61532e62',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51n7ZgLIQlL._AC_SL1056_.jpg'
            },
            {
            'title': 'HP OfficeJet Pro 7740',
            'subTitle': 'The cheap-to-buy, cost-more-per-page option. For low volume',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01JUCLLGK/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01JUCLLGK&linkId=a1332f3ba74345adb5eee8561a38162b',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/81%2BnFIUJLdL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}    
    #112
    if color_type=="black and white" and conc_type=="Ethernet Wired" and paper_size=="Letter Legal 11x17" and print_type=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh MP2501SP',
            'subTitle': 'The sturdy option. Low cost of operation.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B00KDU9Q34/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B00KDU9Q34&linkId=298e6bd25a4db461de0bd9fdfd706b3f',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51mneBb5RML._AC_SL1000_.jpg'
            },
            {
            'title': 'HP OfficeJet Pro 7740',
            'subTitle': 'The cheap-to-buy, cost-more-per-page option.Use only for very low volume',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01JUCLLGK/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01JUCLLGK&linkId=a1332f3ba74345adb5eee8561a38162b',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/81%2BnFIUJLdL._AC_SL1500_.jpg'
            }
            
        ]
        }
        
    }
}   
    #1123
    if color_type=="black and white" and conc_type=="Ethernet Wired" and paper_size=="Letter Legal 11x17" and print_type=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh MP2501SP',
            'subTitle': 'The sturdy option. Low cost of operation.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B00KDU9Q34/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B00KDU9Q34&linkId=298e6bd25a4db461de0bd9fdfd706b3f',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51mneBb5RML._AC_SL1000_.jpg'
            },
            {
            'title': 'HP OfficeJet Pro 7740',
            'subTitle': 'The cheap-to-buy, cost-more-per-page option. Use only for very low volume',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01JUCLLGK/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01JUCLLGK&linkId=a1332f3ba74345adb5eee8561a38162b',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/81%2BnFIUJLdL._AC_SL1500_.jpg'
            }
            
        ]
        }
        
    }
}   
    #1212
    if color_type=="black and white" and conc_type=="WiFi Wireless" and paper_size=="Letter Legal" and print_type=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother Brother MFC-L2750dw  .'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}
    #1213
    if color_type=="black and white" and conc_type=="WiFi Wireless" and paper_size=="Letter Legal" and print_type=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother MFC-L2750dw.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}

    #1131
    if color_type=="black and white" and conc_type=="Ethernet Wired" and paper_size=="24\"-44\" Wide Format" and print_type=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh SP 6430DN',
            'subTitle': 'Ricoh SP 6430DN. The sturdy, low cost per page option.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01132XDD4/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01132XDD4&linkId=1a6d750fc8b8a2ae6daebb4b61532e62',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51n7ZgLIQlL._AC_SL1056_.jpg'
            },
            {
            'title': 'HP OfficeJet Pro 7740',
            'subTitle': 'The cheap-to-buy, cost-more-per-page option. For low volume',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01JUCLLGK/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01JUCLLGK&linkId=a1332f3ba74345adb5eee8561a38162b',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/81%2BnFIUJLdL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
} 

    #1132
    if color_type=="black and white" and conc_type=="Ethernet Wired" and paper_size=="24\"-44\" Wide Format" and print_type=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother Brother MFC-L2750dw  . I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}

    #1133
    if color_type=="black and white" and conc_type=="Ethernet Wired" and paper_size=="24\"-44\" Wide Format" and print_type=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.Brother MFC-L2750dw'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}
    #1233
    if color_type=="black and white" and conc_type=="WiFi Wireless" and paper_size=="24\"-44\" Wide Format" and print_type=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.Brother MFC-L2750dw'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}

    #1232
    if color_type=="black and white" and conc_type=="WiFi Wireless" and paper_size=="24\"-44\" Wide Format" and print_type=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother Brother MFC-L2750dw  . I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}
    #1231
    if color_type=="black and white" and conc_type=="WiFi Wireless" and paper_size=="24\"-44\" Wide Format" and print_type=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh SP 6430DN',
            'subTitle': 'Ricoh SP 6430DN. The sturdy, low cost per page option.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01132XDD4/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01132XDD4&linkId=1a6d750fc8b8a2ae6daebb4b61532e62',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51n7ZgLIQlL._AC_SL1056_.jpg'
            },
            {
            'title': 'HP OfficeJet Pro 7740',
            'subTitle': 'The cheap-to-buy, cost-more-per-page option. For low volume',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01JUCLLGK/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01JUCLLGK&linkId=a1332f3ba74345adb5eee8561a38162b',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/81%2BnFIUJLdL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
} 

    #1221
    if color_type=="black and white" and conc_type=="WiFi Wireless" and paper_size=="Letter Legal 11x17" and print_type=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh MP2501SP',
            'subTitle': 'The sturdy option. Low cost of operation.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B00KDU9Q34/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B00KDU9Q34&linkId=298e6bd25a4db461de0bd9fdfd706b3f',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51mneBb5RML._AC_SL1000_.jpg'
            },
            {
            'title': 'HP OfficeJet Pro 7740',
            'subTitle': 'The cheap-to-buy, cost-more-per-page option. Use only for very low volume',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01JUCLLGK/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01JUCLLGK&linkId=a1332f3ba74345adb5eee8561a38162b',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/81%2BnFIUJLdL._AC_SL1500_.jpg'
            }
            
        ]
        }
        
    }
}   

    #1222
    if color_type=="black and white" and conc_type=="WiFi Wireless" and paper_size=="Letter Legal 11x17" and print_type=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh MP2501SP',
            'subTitle': 'The sturdy option. Low cost of operation.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B00KDU9Q34/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B00KDU9Q34&linkId=298e6bd25a4db461de0bd9fdfd706b3f',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51mneBb5RML._AC_SL1000_.jpg'
            },
            {
            'title': 'HP OfficeJet Pro 7740',
            'subTitle': 'The cheap-to-buy, cost-more-per-page option. Use only for very low volume',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01JUCLLGK/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01JUCLLGK&linkId=a1332f3ba74345adb5eee8561a38162b',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/81%2BnFIUJLdL._AC_SL1500_.jpg'
            }
            
        ]
        }
        
    }
}   
    #1223
    if color_type=="black and white" and conc_type=="WiFi Wireless" and paper_size=="Letter Legal 11x17" and print_type=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh MP2501SP',
            'subTitle': 'The sturdy option. Low cost of operation.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B00KDU9Q34/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B00KDU9Q34&linkId=298e6bd25a4db461de0bd9fdfd706b3f',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51mneBb5RML._AC_SL1000_.jpg'
            },
            {
            'title': 'HP OfficeJet Pro 7740',
            'subTitle': 'The cheap-to-buy, cost-more-per-page option. Use only for very low volume',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01JUCLLGK/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01JUCLLGK&linkId=a1332f3ba74345adb5eee8561a38162b',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/81%2BnFIUJLdL._AC_SL1500_.jpg'
            }
            
        ]
        }
        
    }
}   

    #2111
    if color_type=="color" and conc_type=="Ethernet Wired" and paper_size=="Letter Legal" and print_type=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.  HP Color Laserjet Pro M254dw '
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Color Laserjet Pro M254dw',
            'subTitle': 'HP Color Laserjet Pro M254dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B073R2WVKB/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B073R2WVKB&linkId=ec37523e25f2470d1647c3ac210307ca',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61Djm6Rig9L._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2112
    if color_type=="color" and conc_type=="Ethernet Wired" and paper_size=="Letter Legal" and print_type=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Color Laserjet Pro MFP M281fdw.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Color Laserjet Pro MFP M281fdw',
            'subTitle': 'HP Color Laserjet Pro MFP M281fdw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B073RG8Z72/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B073RG8Z72&linkId=197318e01fad128465491ec5ab36a9ca',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61aYZRJ-zoL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2113
    if color_type=="color" and conc_type=="Ethernet Wired" and paper_size=="Letter Legal" and print_type=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Color Laserjet Pro MFP M281fdw.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Color Laserjet Pro MFP M281fdw',
            'subTitle': 'HP Color Laserjet Pro MFP M281fdw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B073RG8Z72/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B073RG8Z72&linkId=197318e01fad128465491ec5ab36a9ca',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61aYZRJ-zoL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}

    #2121
    if color_type=="color" and conc_type=="Ethernet Wired" and paper_size=="Letter Legal 11x17" and print_type=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Color Laserjet Pro MFP M281fdw.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Lexmark CS923de',
            'subTitle': 'This printer is pricey, but rock solid.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B074VLXCW7/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B074VLXCW7&linkId=acfa0e5e13d49fde0ecec4a47792ad25',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/817z9pbUXqL._SL1500_.jpg'
            }
            
        ]
        }
    }
}

    #2122
    if color_type=="color" and conc_type=="Ethernet Wired" and paper_size=="Letter Legal 11x17" and print_type=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh C2004ex',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7548/Ricoh-MP-C2004ex-Color-Laser-Multifunction-Copier',
            'imageUrl': 'https://copyfaxes.com/media/p/o/4d644bd6_ricoh_c2004ex.png'
            },
            {
            'title': 'Konica Minolta C227',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7145/Konica-Minolta-Bizhub-C227-Copier-Printer-Scanner?utm_source=productlistingads&utm_medium=adwords&utm_campaign=adwords&gclid=EAIaIQobChMI_rG2-Kff3gIVDr7ACh14SgOsEAQYASABEgKc0PD_BwE',
            'imageUrl': 'https://copyfaxes.com/media/p/o/3bf7274d_c227.jpeg'
            }
            
        ]
        }
        
    }
}   
    #2123
    if color_type=="color" and conc_type=="Ethernet Wired" and paper_size=="Letter Legal 11x17" and print_type=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh C2004ex',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7548/Ricoh-MP-C2004ex-Color-Laser-Multifunction-Copier',
            'imageUrl': 'https://copyfaxes.com/media/p/o/4d644bd6_ricoh_c2004ex.png'
            },
            {
            'title': 'Konica Minolta C227',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7145/Konica-Minolta-Bizhub-C227-Copier-Printer-Scanner?utm_source=productlistingads&utm_medium=adwords&utm_campaign=adwords&gclid=EAIaIQobChMI_rG2-Kff3gIVDr7ACh14SgOsEAQYASABEgKc0PD_BwE',
            'imageUrl': 'https://copyfaxes.com/media/p/o/3bf7274d_c227.jpeg'
            }
            
        ]
        }
        
    }
}  
    #2211
    if color_type=="color" and conc_type=="WiFi Wireless" and paper_size=="Letter Legal" and print_type=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.  HP Color Laserjet Pro M254dw '
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Color Laserjet Pro M254dw',
            'subTitle': 'HP Color Laserjet Pro M254dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B073R2WVKB/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B073R2WVKB&linkId=ec37523e25f2470d1647c3ac210307ca',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61Djm6Rig9L._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2212
    if color_type=="color" and conc_type=="WiFi Wireless" and paper_size=="Letter Legal" and print_type=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Color Laserjet Pro MFP M281fdw.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Color Laserjet Pro MFP M281fdw',
            'subTitle': 'HP Color Laserjet Pro MFP M281fdw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B073RG8Z72/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B073RG8Z72&linkId=197318e01fad128465491ec5ab36a9ca',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61aYZRJ-zoL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}

    #2213
    if color_type=="color" and conc_type=="WiFi Wireless" and paper_size=="Letter Legal" and print_type=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Color Laserjet Pro MFP M281fdw.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Color Laserjet Pro MFP M281fdw',
            'subTitle': 'HP Color Laserjet Pro MFP M281fdw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B073RG8Z72/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B073RG8Z72&linkId=197318e01fad128465491ec5ab36a9ca',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61aYZRJ-zoL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2221
    if color_type=="color" and conc_type=="WiFi Wireless" and paper_size=="Letter Legal 11x17" and print_type=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Lexmark CS923de'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Lexmark CS923de',
            'subTitle': 'This printer is pricey, but rock solid.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B074VLXCW7/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B074VLXCW7&linkId=acfa0e5e13d49fde0ecec4a47792ad25',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/817z9pbUXqL._SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2222
    if color_type=="color" and conc_type=="WiFi Wireless" and paper_size=="Letter Legal 11x17" and print_type=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh C2004ex',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7548/Ricoh-MP-C2004ex-Color-Laser-Multifunction-Copier',
            'imageUrl': 'https://copyfaxes.com/media/p/o/4d644bd6_ricoh_c2004ex.png'
            },
            {
            'title': 'Konica Minolta C227',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7145/Konica-Minolta-Bizhub-C227-Copier-Printer-Scanner?utm_source=productlistingads&utm_medium=adwords&utm_campaign=adwords&gclid=EAIaIQobChMI_rG2-Kff3gIVDr7ACh14SgOsEAQYASABEgKc0PD_BwE',
            'imageUrl': 'https://copyfaxes.com/media/p/o/3bf7274d_c227.jpeg'
            }
            
        ]
        }
        
    }
}  
    #2223
    if color_type=="color" and conc_type=="WiFi Wireless" and paper_size=="Letter Legal 11x17" and print_type=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh C2004ex',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7548/Ricoh-MP-C2004ex-Color-Laser-Multifunction-Copier',
            'imageUrl': 'https://copyfaxes.com/media/p/o/4d644bd6_ricoh_c2004ex.png'
            },
            {
            'title': 'Konica Minolta C227',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7145/Konica-Minolta-Bizhub-C227-Copier-Printer-Scanner?utm_source=productlistingads&utm_medium=adwords&utm_campaign=adwords&gclid=EAIaIQobChMI_rG2-Kff3gIVDr7ACh14SgOsEAQYASABEgKc0PD_BwE',
            'imageUrl': 'https://copyfaxes.com/media/p/o/3bf7274d_c227.jpeg'
            }
            
        ]
        }
        
    }
}  
    #2231
    if color_type=="color" and conc_type=="WiFi Wireless" and paper_size=="24\"-44\" Wide Format" and print_type=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Designjet T520 36'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Designjet T520 36',
            'subTitle': 'I\'m a fan of HP\'s Designjets. They are reliable and serviceable.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B009ERB6JE/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B009ERB6JE&linkId=0ca1d67addbb131d548f8851940f76c6',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41vn2nZHndL.jpg'
            }
            
        ]
        }
    }
}
    #2131
    if color_type=="color" and conc_type=="Ethernet Wired" and paper_size=="24\"-44\" Wide Format" and print_type=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Designjet T520 36'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Designjet T520 36',
            'subTitle': 'I\'m a fan of HP\'s Designjets. They are reliable and serviceable.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B009ERB6JE/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B009ERB6JE&linkId=0ca1d67addbb131d548f8851940f76c6',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41vn2nZHndL.jpg'
            }
            
        ]
        }
    }
}
    #2132
    if color_type=="color" and conc_type=="Ethernet Wired" and paper_size=="24\"-44\" Wide Format" and print_type=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Designjet T520 36'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Designjet T830 MFP 36"',
            'subTitle': ' I\'m a fan of HP\'s Designjets. They are reliable and serviceable.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B017V5LFLO/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B017V5LFLO&linkId=d25fa8081bbc02b2bc5d8aac596db248',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/91NLa8MjqpL._SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2232
    if color_type=="color" and conc_type=="WiFi Wireless" and paper_size=="24\"-44\" Wide Format" and print_type=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Designjet T520 36'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Designjet T520 36',
            'subTitle': ' I\'m a fan of HP\'s Designjets. They are reliable and serviceable.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B017V5LFLO/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B017V5LFLO&linkId=d25fa8081bbc02b2bc5d8aac596db248',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/91NLa8MjqpL._SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2233
    if color_type=="color" and conc_type=="WiFi Wireless" and paper_size=="24\"-44\" Wide Format" and print_type=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Designjet T520 36'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Designjet T830 MFP 36"',
            'subTitle': 'I\'m a fan of HP\'s Designjets. They are reliable and serviceable.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B017V5LFLO/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B017V5LFLO&linkId=d25fa8081bbc02b2bc5d8aac596db248',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/91NLa8MjqpL._SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2133
    if color_type=="color" and conc_type=="Ethernet Wired" and paper_size=="24\"-44\" Wide Format" and print_type=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Designjet T520 36'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Designjet T830 MFP 36"',
            'subTitle': 'I\'m a fan of HP\'s Designjets. They are reliable and serviceable.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B017V5LFLO/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B017V5LFLO&linkId=d25fa8081bbc02b2bc5d8aac596db248',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/91NLa8MjqpL._SL1500_.jpg'
            }
            
        ]
        }
    }
}









def get_recommendationa(intent_request):
    """
    

    Beyond fulfillment, the implementation for this intent demonstrates the following:
    1) Use of elicitSlot in slot validation and re-prompting
    2) Use of sessionAttributes to pass information that can be used to guide conversation
    """

    color_typea = try_ex(lambda: intent_request['currentIntent']['slots']['slotSup'])
    conc_typea = try_ex(lambda: intent_request['currentIntent']['slots']['slotBap'])
    

    paper_sizea = try_ex(lambda: intent_request['currentIntent']['slots']['slotBan'])
    print_typea = try_ex(lambda: intent_request['currentIntent']['slots']['slotRan'])
    
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    # Load confirmation history and track the current reservation.
    reservation = json.dumps({
        'color_typea': color_typea,
        'conc_typea': color_typea,
        'PaperSizea': paper_sizea,
        'Print-typea': print_typea,
    
    })

    session_attributes['currentReservation'] = reservation

    
    validation_result = validate_machinesa(intent_request['currentIntent']['slots'])
    if not validation_result['isValid']:
        slots = intent_request['currentIntent']['slots']
        slots[validation_result['violatedSlot']] = None

        return elicit_slot(
            session_attributes,
            intent_request['currentIntent']['name'],
            slots,
            validation_result['violatedSlot'],
            validation_result['message']
        )

    #1111    
    if color_typea=="black and white" and conc_typea=="Ethernet Wired" and paper_sizea=="Letter Legal" and print_typea=="Print Only":
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother HL-L2350DW   $99 . '
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP LaserJet Enterprise M607dn',
            'subTitle': 'HP LaserJet Enterprise M607dn',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B0716YY61S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B0716YY61S&linkId=87c68a999365ed7f23b476351b8918c0',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/71bop1%2Be5SL._SL1500_.jpg'
            },
            {
            'title': 'JetDirect 3100',
            'subTitle': 'For Wifi, NFC, or other wireless options you will need to add a JetDirect 3100.',
            'attachmentLinkUrl': 'https://www.provantage.com/hp-3jn69a~7HEWE1Y5.htm',
            'imageUrl': 'https://www.provantage.com/1049378042.JPG'
            }
            
        ]
        }
    }
}

    #1112
    if color_typea=="black and white" and conc_typea=="Ethernet Wired" and paper_sizea=="Letter Legal" and print_typea=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother Brother MFC-L2750dw  . I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP LaserJet MFP M521dn',
            'subTitle': 'HP LaserJet MFP M521dn',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B06XC57LNB/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B06XC57LNB&linkId=e19582c23bcf02a4bd52558b54d5f9b4',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/6177R7EJl0L._SL1500_.jpg'
            }
            
        ]
        }
    }
}

    #1113
    if color_typea=="black and white" and conc_typea=="Ethernet Wired" and paper_sizea=="Letter Legal" and print_typea=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother Brother MFC-L2750dw  . I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP LaserJet MFP M521dn',
            'subTitle': 'HP LaserJet MFP M521dn',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B06XC57LNB/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B06XC57LNB&linkId=e19582c23bcf02a4bd52558b54d5f9b4',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/6177R7EJl0L._SL1500_.jpg'
            }
            
        ]
        }
    }
}
    
    #1211
    if color_typea=="black and white" and conc_typea=="WiFi Wireless" and paper_sizea=="Letter Legal" and print_typea=="Print Only":
        
       return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother HL-L2350DW   $99 . '
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP LaserJet Enterprise M607dn',
            'subTitle': 'HP LaserJet Enterprise M607dn',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B0716YY61S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B0716YY61S&linkId=87c68a999365ed7f23b476351b8918c0',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/71bop1%2Be5SL._SL1500_.jpg'
            },
            {
            'title': 'JetDirect 3100',
            'subTitle': 'For Wifi, NFC, or other wireless options you will need to add a JetDirect 3100.',
            'attachmentLinkUrl': 'https://www.provantage.com/hp-3jn69a~7HEWE1Y5.htm',
            'imageUrl': 'https://www.provantage.com/1049378042.JPG'
            }
            
        ]
        }
    }
}   
    #1121
    if color_typea=="black and white" and conc_typea=="Ethernet Wired" and paper_sizea=="Letter Legal 11x17" and print_typea=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh SP 6430DN',
            'subTitle': 'Ricoh SP 6430DN. The sturdy, low cost per page option.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01132XDD4/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01132XDD4&linkId=1a6d750fc8b8a2ae6daebb4b61532e62',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51n7ZgLIQlL._AC_SL1056_.jpg'
            }
          
        ]
        }
    }
}    
    #1122
    if color_typea=="black and white" and conc_typea=="Ethernet Wired" and paper_sizea=="Letter Legal 11x17" and print_typea=="Print Copy Scan":
        
       return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.Brother MFC-L2750dw'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}  
    #1123
    if color_typea=="black and white" and conc_typea=="Ethernet Wired" and paper_sizea=="Letter Legal 11x17" and print_typea=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.Brother MFC-L2750dw'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}  
    #1212
    if color_typea=="black and white" and conc_typea=="WiFi Wireless" and paper_sizea=="Letter Legal" and print_typea=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother Brother MFC-L2750dw  . I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP LaserJet MFP M521dn',
            'subTitle': 'HP LaserJet MFP M521dn',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B06XC57LNB/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B06XC57LNB&linkId=e19582c23bcf02a4bd52558b54d5f9b4',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/6177R7EJl0L._SL1500_.jpg'
            },
            {
            'title': 'My recommendation is to connect via ethernet.',
            'subTitle': 'If you want the printer to connect wirelessly, get this print server:',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B002TIOXMC/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B002TIOXMC&linkId=f88ad86dbdaa37de195d4d96021f1cb6',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/81ar9M4b7iL._SL1500_.jpg'
                
            }
            
        ]
        }
    }
}
    #1213
    if color_typea=="black and white" and conc_typea=="WiFi Wireless" and paper_sizea=="Letter Legal" and print_typea=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother Brother MFC-L2750dw  . I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP LaserJet MFP M521dn',
            'subTitle': 'HP LaserJet MFP M521dn',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B06XC57LNB/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B06XC57LNB&linkId=e19582c23bcf02a4bd52558b54d5f9b4',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/6177R7EJl0L._SL1500_.jpg'
            },
            {
            'title': 'My recommendation is to connect via ethernet.',
            'subTitle': 'If you want the printer to connect wirelessly, get this print server:',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B002TIOXMC/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B002TIOXMC&linkId=f88ad86dbdaa37de195d4d96021f1cb6',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/81ar9M4b7iL._SL1500_.jpg'
                
            }
            
        ]
        }
    }
}

    #1131
    if color_typea=="black and white" and conc_typea=="Ethernet Wired" and paper_sizea=="24\"-44\" Wide Format" and print_typea=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh SP 6430DN',
            'subTitle': 'Ricoh SP 6430DN. The sturdy, low cost per page option.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01132XDD4/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01132XDD4&linkId=1a6d750fc8b8a2ae6daebb4b61532e62',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51n7ZgLIQlL._AC_SL1056_.jpg'
            }
            
        ]
        }
    }
} 

    #1132
    if color_typea=="black and white" and conc_typea=="Ethernet Wired" and paper_sizea=="24\"-44\" Wide Format" and print_typea=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother Brother MFC-L2750dw  . I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}

    #1133
    if color_typea=="black and white" and conc_typea=="Ethernet Wired" and paper_sizea=="24\"-44\" Wide Format" and print_typea=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.Brother MFC-L2750dw'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}
    #1233
    if color_typea=="black and white" and conc_typea=="WiFi Wireless" and paper_sizea=="24\"-44\" Wide Format" and print_typea=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.Brother MFC-L2750dw'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}

    #1232
    if color_typea=="black and white" and conc_typea=="WiFi Wireless" and paper_sizea=="24\"-44\" Wide Format" and print_typea=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother Brother MFC-L2750dw  . I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
}
    #1231
    if color_typea=="black and white" and conc_typea=="WiFi Wireless" and paper_sizea=="24\"-44\" Wide Format" and print_typea=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh SP 6430DN',
            'subTitle': 'Ricoh SP 6430DN. The sturdy, low cost per page option.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01132XDD4/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01132XDD4&linkId=1a6d750fc8b8a2ae6daebb4b61532e62',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51n7ZgLIQlL._AC_SL1056_.jpg'
            }
        ]
        }
    }
} 

    #1221
    if color_typea=="black and white" and conc_typea=="WiFi Wireless" and paper_sizea=="Letter Legal 11x17" and print_typea=="Print Only":
        
         return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh SP 6430DN',
            'subTitle': 'Ricoh SP 6430DN will require an external print server to connect wirelessly',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B01132XDD4/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B01132XDD4&linkId=1a6d750fc8b8a2ae6daebb4b61532e62',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51n7ZgLIQlL._AC_SL1056_.jpg'
            },
            {
            'title': 'Ricoh external print server type O',
            'subTitle': 'Ricoh external print server type O',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B00E7MNSQK/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B00E7MNSQK&linkId=87af630754bce197af1cf31afa52bfbe',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/816dHTg9E4L._SL1500_.jpg'
            }
            
        ]
        }
    }
} 

    #1222
    if color_typea=="black and white" and conc_typea=="WiFi Wireless" and paper_sizea=="Letter Legal 11x17" and print_typea=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother Brother MFC-L2750dw  . I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
} 
    #1223
    if color_typea=="black and white" and conc_typea=="WiFi Wireless" and paper_sizea=="Letter Legal 11x17" and print_typea=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Brother Brother MFC-L2750dw  . I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Brother MFC-L2750dw',
            'subTitle': 'Brother MFC-L2750dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B077Y5922S/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B077Y5922S&linkId=15908bce66e4353187727c321c4c5f32',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41QmG1bfeHL._AC_.jpg'
            }
            
        ]
        }
    }
} 

    #2111
    if color_typea=="color" and conc_typea=="Ethernet Wired" and paper_sizea=="Letter Legal" and print_typea=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.  HP Color Laserjet Pro M254dw '
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Color Laserjet Pro M254dw',
            'subTitle': 'HP Color Laserjet Pro M254dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B073R2WVKB/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B073R2WVKB&linkId=ec37523e25f2470d1647c3ac210307ca',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61Djm6Rig9L._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2112
    if color_typea=="color" and conc_typea=="Ethernet Wired" and paper_sizea=="Letter Legal" and print_typea=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Color Laserjet Pro MFP M281fdw.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Color Laserjet Pro MFP M281fdw',
            'subTitle': 'HP Color Laserjet Pro MFP M281fdw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B073RG8Z72/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B073RG8Z72&linkId=197318e01fad128465491ec5ab36a9ca',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61aYZRJ-zoL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2113
    if color_typea=="color" and conc_typea=="Ethernet Wired" and paper_sizea=="Letter Legal" and print_typea=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Color Laserjet Pro MFP M281fdw.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Color Laserjet Pro MFP M281fdw',
            'subTitle': 'HP Color Laserjet Pro MFP M281fdw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B073RG8Z72/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B073RG8Z72&linkId=197318e01fad128465491ec5ab36a9ca',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61aYZRJ-zoL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}

    #2121
    if color_typea=="color" and conc_typea=="Ethernet Wired" and paper_sizea=="Letter Legal 11x17" and print_typea=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Color Laserjet Pro MFP M281fdw.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Lexmark CS923de',
            'subTitle': 'This printer is pricey, but rock solid.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B074VLXCW7/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B074VLXCW7&linkId=acfa0e5e13d49fde0ecec4a47792ad25',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/817z9pbUXqL._SL1500_.jpg'
            }
            
        ]
        }
    }
}

    #2122
    if color_typea=="color" and conc_typea=="Ethernet Wired" and paper_sizea=="Letter Legal 11x17" and print_typea=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh C2004ex',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7548/Ricoh-MP-C2004ex-Color-Laser-Multifunction-Copier',
            'imageUrl': 'https://copyfaxes.com/media/p/o/4d644bd6_ricoh_c2004ex.png'
            },
            {
            'title': 'Konica Minolta C227',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7145/Konica-Minolta-Bizhub-C227-Copier-Printer-Scanner?utm_source=productlistingads&utm_medium=adwords&utm_campaign=adwords&gclid=EAIaIQobChMI_rG2-Kff3gIVDr7ACh14SgOsEAQYASABEgKc0PD_BwE',
            'imageUrl': 'https://copyfaxes.com/media/p/o/3bf7274d_c227.jpeg'
            }
            
        ]
        }
        
    }
}   
    #2123
    if color_typea=="color" and conc_typea=="Ethernet Wired" and paper_sizea=="Letter Legal 11x17" and print_typea=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh C2004ex',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7548/Ricoh-MP-C2004ex-Color-Laser-Multifunction-Copier',
            'imageUrl': 'https://copyfaxes.com/media/p/o/4d644bd6_ricoh_c2004ex.png'
            },
            {
            'title': 'Konica Minolta C227',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7145/Konica-Minolta-Bizhub-C227-Copier-Printer-Scanner?utm_source=productlistingads&utm_medium=adwords&utm_campaign=adwords&gclid=EAIaIQobChMI_rG2-Kff3gIVDr7ACh14SgOsEAQYASABEgKc0PD_BwE',
            'imageUrl': 'https://copyfaxes.com/media/p/o/3bf7274d_c227.jpeg'
            }
            
        ]
        }
        
    }
}  
    #2211
    if color_typea=="color" and conc_typea=="WiFi Wireless" and paper_sizea=="Letter Legal" and print_typea=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.  HP Color Laserjet Pro M254dw '
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Color Laserjet Pro M254dw',
            'subTitle': 'HP Color Laserjet Pro M254dw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B073R2WVKB/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B073R2WVKB&linkId=ec37523e25f2470d1647c3ac210307ca',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61Djm6Rig9L._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2212
    if color_typea=="color" and conc_typea=="WiFi Wireless" and paper_sizea=="Letter Legal" and print_typea=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Color Laserjet Pro MFP M281fdw.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Color Laserjet Pro MFP M281fdw',
            'subTitle': 'HP Color Laserjet Pro MFP M281fdw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B073RG8Z72/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B073RG8Z72&linkId=197318e01fad128465491ec5ab36a9ca',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61aYZRJ-zoL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}

    #2213
    if color_typea=="color" and conc_typea=="WiFi Wireless" and paper_sizea=="Letter Legal" and print_typea=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Color Laserjet Pro MFP M281fdw.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Color Laserjet Pro MFP M281fdw',
            'subTitle': 'HP Color Laserjet Pro MFP M281fdw',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B073RG8Z72/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B073RG8Z72&linkId=197318e01fad128465491ec5ab36a9ca',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/61aYZRJ-zoL._AC_SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2221
    if color_typea=="color" and conc_typea=="WiFi Wireless" and paper_sizea=="Letter Legal 11x17" and print_typea=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   Lexmark CS923de'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Lexmark CS923de',
            'subTitle': 'This printer is pricey, but rock solid.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B074VLXCW7/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B074VLXCW7&linkId=acfa0e5e13d49fde0ecec4a47792ad25',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/817z9pbUXqL._SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2222
    if color_typea=="color" and conc_typea=="WiFi Wireless" and paper_sizea=="Letter Legal 11x17" and print_typea=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh C2004ex',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7548/Ricoh-MP-C2004ex-Color-Laser-Multifunction-Copier',
            'imageUrl': 'https://copyfaxes.com/media/p/o/4d644bd6_ricoh_c2004ex.png'
            },
            {
            'title': 'Konica Minolta C227',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7145/Konica-Minolta-Bizhub-C227-Copier-Printer-Scanner?utm_source=productlistingads&utm_medium=adwords&utm_campaign=adwords&gclid=EAIaIQobChMI_rG2-Kff3gIVDr7ACh14SgOsEAQYASABEgKc0PD_BwE',
            'imageUrl': 'https://copyfaxes.com/media/p/o/3bf7274d_c227.jpeg'
            }
            
        ]
        }
        
    }
}  
    #2223
    if color_typea=="color" and conc_typea=="WiFi Wireless" and paper_sizea=="Letter Legal 11x17" and print_typea=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'Ricoh C2004ex',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7548/Ricoh-MP-C2004ex-Color-Laser-Multifunction-Copier',
            'imageUrl': 'https://copyfaxes.com/media/p/o/4d644bd6_ricoh_c2004ex.png'
            },
            {
            'title': 'Konica Minolta C227',
            'subTitle': 'Will grow with you. Wireless is an option you buy.',
            'attachmentLinkUrl': 'https://copyfaxes.com/product/7145/Konica-Minolta-Bizhub-C227-Copier-Printer-Scanner?utm_source=productlistingads&utm_medium=adwords&utm_campaign=adwords&gclid=EAIaIQobChMI_rG2-Kff3gIVDr7ACh14SgOsEAQYASABEgKc0PD_BwE',
            'imageUrl': 'https://copyfaxes.com/media/p/o/3bf7274d_c227.jpeg'
            }
            
        ]
        }
        
    }
}  
    #2231
    if color_typea=="color" and conc_typea=="WiFi Wireless" and paper_sizea=="24\"-44\" Wide Format" and print_typea=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Designjet T520 36'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Designjet T520 36',
            'subTitle': 'I\'m a fan of HP\'s Designjets. They are reliable and serviceable.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B009ERB6JE/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B009ERB6JE&linkId=0ca1d67addbb131d548f8851940f76c6',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41vn2nZHndL.jpg'
            }
            
        ]
        }
    }
}
    #2131
    if color_typea=="color" and conc_typea=="Ethernet Wired" and paper_sizea=="24\"-44\" Wide Format" and print_typea=="Print Only":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Designjet T520 36'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Designjet T520 36',
            'subTitle': 'I\'m a fan of HP\'s Designjets. They are reliable and serviceable.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B009ERB6JE/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B009ERB6JE&linkId=0ca1d67addbb131d548f8851940f76c6',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/41vn2nZHndL.jpg'
            }
            
        ]
        }
    }
}
    #2132
    if color_typea=="color" and conc_typea=="Ethernet Wired" and paper_sizea=="24\"-44\" Wide Format" and print_typea=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Designjet T520 36'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Designjet T830 MFP 36"',
            'subTitle': ' I\'m a fan of HP\'s Designjets. They are reliable and serviceable.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B017V5LFLO/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B017V5LFLO&linkId=d25fa8081bbc02b2bc5d8aac596db248',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/91NLa8MjqpL._SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2232
    if color_typea=="color" and conc_typea=="WiFi Wireless" and paper_sizea=="24\"-44\" Wide Format" and print_typea=="Print Copy Scan":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Designjet T520 36'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Designjet T830 MFP 36"',
            'subTitle': ' I\'m a fan of HP\'s Designjets. They are reliable and serviceable.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B017V5LFLO/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B017V5LFLO&linkId=d25fa8081bbc02b2bc5d8aac596db248',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/91NLa8MjqpL._SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2233
    if color_typea=="color" and conc_typea=="WiFi Wireless" and paper_sizea=="24\"-44\" Wide Format" and print_typea=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Designjet T520 36'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Designjet T830 MFP 36"',
            'subTitle': 'I\'m a fan of HP\'s Designjets. They are reliable and serviceable.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B017V5LFLO/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B017V5LFLO&linkId=d25fa8081bbc02b2bc5d8aac596db248',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/91NLa8MjqpL._SL1500_.jpg'
            }
            
        ]
        }
    }
}
    #2133
    if color_typea=="color" and conc_typea=="Ethernet Wired" and paper_sizea=="24\"-44\" Wide Format" and print_typea=="Print Copy Scan Fax":
        
        return {
    'dialogAction': {
        'type': 'Close',
        'fulfillmentState': 'Fulfilled',
        'message': {
            'contentType': 'PlainText',
            'content': 'Great! I have a recommendation for you. I\'ll send it now with a link to Amazon.   HP Designjet T520 36'
        },
        'responseCard': {
        'version': '0',
        'contentType': 'application/vnd.amazonaws.card.generic',
        'genericAttachments': [
            {
            'title': 'HP Designjet T520 36',
            'subTitle': 'I\'m a fan of HP\'s Designjets. They are reliable and serviceable.',
            'attachmentLinkUrl': 'https://www.amazon.com/gp/product/B017V5LFLO/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=mondayswith0f-20&creative=9325&linkCode=as2&creativeASIN=B017V5LFLO&linkId=d25fa8081bbc02b2bc5d8aac596db248',
            'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/91NLa8MjqpL._SL1500_.jpg'
            }
            
        ]
        }
    }
}







# --- Intents ---


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'QuizContinue':
        return get_recommendation(intent_request)
    if intent_name == 'QuizContinueA':
        return get_recommendationa(intent_request)    

    #raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
