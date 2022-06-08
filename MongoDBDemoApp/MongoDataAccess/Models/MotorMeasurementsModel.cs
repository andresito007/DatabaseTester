using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System;

namespace MongoDataAccess.Models
{
    public class MotorMeasurementsModel
    {
        [BsonId]
        [BsonRepresentation(BsonType.Timestamp)]
        public DateTime ReportTime { get; set; }
        public MotorDescriptionModel MotorDescription { get; set; }
        
        public double Position { get; set; }
        public double Speed { get; set; }
        public double Current { get; set; }
    }
}
