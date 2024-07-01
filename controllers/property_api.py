import json
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request


def invalid_response(error, status):
    response_body = {
        'error': error
    }
    return request.make_json_response(response_body, status=status)


def valid_response(data, status):
    response_body = {
        'message': 'successfully',
        'data': data
    }
    return request.make_json_response(response_body, status=status)


class PropertyApi(http.Controller):

    @http.route('/v1/property', methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):  # create new property from api
        print("inside post_property method")
        # return data (POST/Create) in Body JSON send by user with Postman
        args = request.httprequest.data.decode()
        # converted to format json => dict{} => vals to use in creation =>in order to use it easily in python code
        vals = json.loads(args)
        print(vals)  # {'name': 'Property api 1', 'postcode': '17', 'garden_orientation': 'north', 'bedrooms': '10'}
        # Before sending Data you need to add validation layer
        if not vals.get('name'):
            return request.make_json_response({
                'error': 'Name is required',
            }, status=400)
        # I can handle errors by try/except and handle validation related arguments it depends business
        try:
            # to create use env for values(vals) contains dict
            # to create new property I use creation by super_admin or superuser .sudo()
            res = request.env["property"].sudo().create(vals)
            print(res)
            if res:
                # make_json_response pass two things :
                # 1.dict{} converted json to return user response record  + 2.status_code if successfully==200
                return request.make_json_response({
                    # return to user response record created successfully and created data
                    'message': 'Property has been created successfully',
                    'id': res.id,
                    'name': res.name,
                    # status=200 ok in general
                }, status=201)  # 201 Created indicates that the request was successful and a resource was created
        except Exception as error:  # any Exception or error
            return request.make_json_response({
                'error': error,
            }, status=400)

    @http.route('/v1/property/json', methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        print("inside post_property_json method")
        # return data (POST/Create) in Body JSON send by user with Postman
        args = request.httprequest.data.decode()
        # converted to format json => dict{} => vals to use in creation =>in order to use it easily in python code
        vals = json.loads(args)
        # type="json" does not accept any type other than json otherwise it returns an error 400 Bad Request
        # type="json" I can't handle content type then user send data while type="http" I can it
        print(vals)
        
        res = request.env["property"].sudo().create(vals)
        print(res)
        if res:
            # we don't need to customize the status code & the response by default send {"jsonrpc": "2.0","id": null}
            # & 200 ok and just list[] or dict{}
            # {"jsonrpc": "2.0", "id": null, "result": [{"message": "Property has been created successfully"}]}
            return [{
                'message': 'Property has been created successfully'
            }]

    @http.route('/v1/property/<int:property_id>', methods=["PUT"], type="http", auth="none", csrf=False) #
    # <int:property_id> parametre variable dynamic type integer
    def update_property(self, property_id):  # Update property from api
        # I can handle errors by try/except and handle validation related arguments it depends business
        try:
            property_id = request.env["property"].sudo().search([("id", "=", property_id)])
            print(property_id)
            # Before sending Data you need to add validation layer
            if not property_id:
                return request.make_json_response({
                    'error': 'ID Does not exist',
                }, status=400)
            # return data (update) in Body JSON send by user with Postman
            args = request.httprequest.data.decode()
            # converted to format json => dict{} => vals to use it easily in python code
            vals = json.loads(args)
            print(vals)  # {'garden_area': 600, 'bedrooms': 10}
            # Update property from api
            property_id.write(vals)
            print(property_id.garden_area)  # 600
            print(property_id.bedrooms)     # 10

            return request.make_json_response({
                # return to user response record updated successfully and updated data
                'message': 'Property has been updated successfully',
                'id': property_id.id,
                'name': property_id.name,
            }, status=200)  # 200 updated
        except Exception as error:  # any Exception or error
            return request.make_json_response({
                'error': error,
            }, status=400)

    @http.route('/v1/property/<int:property_id>', methods=["GET"], type="http", auth="none", csrf=False)  #
    # <int:property_id> parametre variable dynamic type integer
    def get_property(self, property_id):  # Read property from api
        # I can handle errors by try/except and handle validation related arguments it depends business
        try:
            property_id = request.env["property"].sudo().search([("id", "=", property_id)])
            print(property_id)
            # Before sending Data you need to add validation layer
            if not property_id:
                # return invalid_response instead request.make_json_response
                return invalid_response('ID Does not exist', 400)

            # return valid_response instead request.make_json_response
            return valid_response({
                # return to user response record read successfully data
                'message': 'Property has been read successfully',
                'id': property_id.id,
                'name': property_id.name,
                'ref': property_id.ref,
                'description': property_id.description,
                'bedrooms': property_id.bedrooms,
            }, 200)  # 200 read
        except Exception as error:  # any Exception or error
            return request.make_json_response({
                'error': error,
            }, status=400)

    @http.route('/v1/property/<int:property_id>', methods=["DELETE"], type="http", auth="none", csrf=False)  #
    # <int:property_id> parametre variable dynamic type integer
    def delete_property(self, property_id):  # Delete property from api
        # I can handle errors by try/except and handle validation related arguments it depends business
        try:
            property_id = request.env["property"].sudo().search([("id", "=", property_id)])
            print(property_id)
            # Before sending Data you need to add validation layer
            if not property_id:
                return request.make_json_response({
                    'error': 'ID Does not exist',
                }, status=400)

            # Delete property from api
            property_id.unlink()
            return request.make_json_response({
                # return to user response record deleted successfully and deleted data
                'message': 'Property has been deleted successfully',
            }, status=200)  # 200 delete
        except Exception as error:  # any Exception or error
            return request.make_json_response({
                'error': error,
            }, status=400)
        
    @http.route('/v1/properties', methods=["GET"], type="http", auth="none", csrf=False)
    # properties Get list of records with filtration
    def get_property_list(self):  # Read/Get list of records:property from api
        # I can handle errors by try/except and handle validation related arguments it depends business
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            print(params)
            # query_string = ?"state=closed"
            # parse_qs(query_string) = {'state'=['closed']}
            property_domain = []  # dynamic because if it's empty  => search[] empty return all records
            if params.get('state'):
                property_domain = [("state", "=", params.get('state')[0])]
            print(property_domain)
            
            # if search[] empty return all records
            property_ids = request.env["property"].sudo().search(property_domain)  # Get [records] with filtration
            print(property_ids)
            # Before sending Data you need to add validation layer
            if not property_ids:
                return request.make_json_response({
                    'error': 'There are not records',
                }, status=400)

            # return valid_response instead request.make_json_response
            return valid_response([{
                # return to user response all records read successfully data
                # 'message': 'Property has been read successfully',
                'id': property_id.id,
                'name': property_id.name,
                'ref': property_id.ref,
                'description': property_id.description,
                'bedrooms': property_id.bedrooms,
                'state': property_id.state,
            } for property_id in property_ids], status=200)  # 200 read
        except Exception as error:  # any Exception or error
            return request.make_json_response({
                'error': error,
            }, status=400)
        
        
        
        
        
