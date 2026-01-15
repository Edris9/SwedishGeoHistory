namespace backend_api.Models;

public class User
{
    public int Id { get; set; }
    public string Role { get; set; } = "";
    public string? Name { get; set; }
    public string? JobTitle { get; set; }
    public string? ProofUrl { get; set; }
    public DateTime CreatedAt { get; set; }
}