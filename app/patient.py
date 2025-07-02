class Patient(object):
  def __init__(self):
    self._id = ''
    self._name = ''
    self._gender = ''
    self._date_of_birth = ''

  def _getID(self):
    return self._id
  
  def _setID(self, id):
    self._id = id

  def _getName(self):
    return self._name
  
  def _setName(self, name):
    self._name = name

  def _getGender(self):
    return self._gender
  
  def _setGender(self, gender):
    self._gender = gender

  def _getDateOfBirth(self):
    return self._date_of_birth
  
  def _setDateOfBirth(self, date_of_birth):
    self._date_of_birth = date_of_birth

  ID = property(_getID, _setID)
  Name = property(_getName, _setName)
  Gender = property(_getGender, _setGender)
  DateOfBirth = property(_getDateOfBirth, _setDateOfBirth)