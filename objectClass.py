class Location:
    def __init__(self, lat, lng, address, city, country):
        self.lat = lat
        self.lng = lng
        self.address = address
        self.city = city
        self.country = country

    @classmethod
    def from_json(cls, data):
        return cls(
            lat=data.get('lat'),
            lng=data.get('lng'),
            address=data.get('address'),
            city=data.get('city'),
            country=data.get('country')
        )

    def to_json(self):
        return {
            "lat": self.lat,
            "lng": self.lng,
            "address": self.address,
            "city": self.city,
            "country": self.country
        }


class Amenities:
    def __init__(self, general, room):
        self.general = general
        self.room = room

    @classmethod
    def from_json(cls, data):
        return cls(
            general=data.get('general'),
            room=data.get('room')
        )

    def to_json(self):
        return {
            "general": self.general,
            "room": self.room
        }


class Image:
    def __init__(self, link, description):
        self.link = link
        self.description = description

    @classmethod
    def from_json(cls, data):
        return cls(
            link=data.get('link'),
            description=data.get('description')
        )

    def to_json(self):
        return {
            "link": self.link,
            "description": self.description
        }


class Images:
    def __init__(self, rooms, site, amenities):
        self.rooms = rooms or []
        self.site = site or []
        self.amenities = amenities or []

    @classmethod
    def from_json(cls, data):
        return cls(
            rooms=[Image.from_json(img) for img in data.get('rooms', [])],
            site=[Image.from_json(img) for img in data.get('site', [])],
            amenities=[Image.from_json(img) for img in data.get('amenities', [])]
        )

    def to_json(self):
        return {
            "rooms": [img.to_json() for img in self.rooms],
            "site": [img.to_json() for img in self.site],
            "amenities": [img.to_json() for img in self.amenities]
        }


class Hotel:
    def __init__(self, id, destination_id, name, description, location, amenities, images, booking_conditions):
        self.id = id
        self.destination_id = destination_id
        self.name = name
        self.description = description
        self.location = location
        self.amenities = amenities
        self.images = images
        self.booking_conditions = booking_conditions or []

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data.get('id'),
            destination_id=data.get('destination_id'),
            name=data.get('name'),
            description=data.get('description'),
            location=Location.from_json(data.get('location', {})),
            amenities=Amenities.from_json(data.get('amenities', {})),
            images=Images.from_json(data.get('images', {})),
            booking_conditions=data.get('booking_conditions', [])
        )

    def to_json(self):
        return {
            "id": self.id,
            "destination_id": self.destination_id,
            "name": self.name,
            "description": self.description,
            "location": self.location.to_json(),
            "amenities": self.amenities.to_json(),
            "images": self.images.to_json(),
            "booking_conditions": self.booking_conditions
        }