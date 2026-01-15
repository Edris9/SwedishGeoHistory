using Microsoft.EntityFrameworkCore;
using backend_api.Models;

namespace backend_api.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<Event> Events { get; set; }
    public DbSet<User> Users { get; set; }
    public DbSet<Issue> Issues { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Event>(e =>
        {
            e.ToTable("events");
            e.Property(x => x.Id).HasColumnName("id");
            e.Property(x => x.Year).HasColumnName("year");
            e.Property(x => x.Title).HasColumnName("title");
            e.Property(x => x.Description).HasColumnName("description");
            e.Property(x => x.Area).HasColumnName("area");
            e.Property(x => x.SourceUrl).HasColumnName("source_url");
            e.Property(x => x.CreatedAt).HasColumnName("created_at");
        });

        modelBuilder.Entity<User>(u =>
        {
            u.ToTable("users");
            u.Property(x => x.Id).HasColumnName("id");
            u.Property(x => x.Role).HasColumnName("role");
            u.Property(x => x.Name).HasColumnName("name");
            u.Property(x => x.JobTitle).HasColumnName("job_title");
            u.Property(x => x.ProofUrl).HasColumnName("proof_url");
            u.Property(x => x.CreatedAt).HasColumnName("created_at");
        });

        modelBuilder.Entity<Issue>(i =>
        {
            i.ToTable("issues");
            i.Property(x => x.Id).HasColumnName("id");
            i.Property(x => x.IssueNumber).HasColumnName("issue_number");
            i.Property(x => x.TeacherId).HasColumnName("teacher_id");
            i.Property(x => x.EventId).HasColumnName("event_id");
            i.Property(x => x.Description).HasColumnName("description");
            i.Property(x => x.Status).HasColumnName("status");
            i.Property(x => x.CreatedAt).HasColumnName("created_at");
        });
    }
}