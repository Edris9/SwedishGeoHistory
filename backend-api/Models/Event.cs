using System.ComponentModel.DataAnnotations.Schema;

namespace backend_api.Models;

public class Event
{
    [Column("id")]
    public int Id { get; set; }
    
    [Column("title")]
    public string Title { get; set; }
    
    [Column("description")]
    public string Description { get; set; }
    
    [Column("year")]
    public int Year { get; set; }
    
    [Column("area")]
    public string? Area { get; set; }
    
    [Column("sourceurl")]
    public string? SourceUrl { get; set; }
    
    [Column("createdat")]
    public DateTime? CreatedAt { get; set; }
}