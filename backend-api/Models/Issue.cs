namespace backend_api.Models;

public class Issue
{
    public int Id { get; set; }
    public string? IssueNumber { get; set; }
    public int? TeacherId { get; set; }
    public int? EventId { get; set; }
    public string Description { get; set; } = "";
    public string Status { get; set; } = "open";
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}